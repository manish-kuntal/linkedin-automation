"""Safe agent orchestration: discover -> analyze -> recommend -> notify -> human review."""
from __future__ import annotations

import logging
import os
import time

from agent.analyzer import Analyzer
from agent.recommender import Recommender
from agent.safety import SafetyEvent, SafetyGuard
from config import PID_FILE, RUNNING_FLAG, SETTINGS, STOP_FILE
from linkedin.discovery import Discovery
from notifications import desktop, telegram
from storage.database import Database

logger = logging.getLogger("agent")
actions_logger = logging.getLogger("actions")


class Orchestrator:
    def __init__(self):
        self.settings = SETTINGS
        self.db = Database()
        self.guard = SafetyGuard(self.db)
        self.analyzer = Analyzer(self.settings)
        self.recommender = Recommender(self.settings)
        self.discovery = Discovery(self.settings)
        self.session_open = False

    def start_session(self):
        problems = self.settings.validate()
        if problems:
            self.guard.raise_safety_event(
                "CONFIG_ERROR",
                "; ".join(problems),
            )

        RUNNING_FLAG.write_text("1", encoding="utf-8")
        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")

        self.db.open_session(self.settings.mode)
        self.session_open = True
        self.db.recover()

        logger.info(
            "Agent started. Mode=%s",
            self.settings.mode,
        )

    def end_session(self, outcome="STOPPED"):
        if self.session_open:
            self.db.close_session(outcome)
            self.session_open = False

        RUNNING_FLAG.unlink(missing_ok=True)
        PID_FILE.unlink(missing_ok=True)

        logger.info(
            "Agent stopped. Outcome=%s",
            outcome,
        )

    def process_post(self, post: dict, force_demo: bool = False):
        post_id = str(post.get("id", "")).strip()

        if not post_id:
            logger.warning("Post without ID skipped.")
            return

        # In SAFE_DEMO we allow the same mock posts to be demonstrated
        # repeatedly. In all other modes, duplicate protection remains active.
        if self.db.post_seen(post_id) and not force_demo:
            logger.info(
                "Duplicate post skipped: %s",
                post_id,
            )
            return

        self.db.upsert_post(
            post_id,
            post.get("author", "Unknown"),
            post.get("url", ""),
            post.get("text", ""),
            post.get("source", "mock"),
        )

        analysis = self.analyzer.analyze(
            post.get("text", "")
        )

        rec = self.recommender.recommend(analysis)

        for suggestion in rec["comment_suggestions"]:
            self.db.save_suggestion(
                post_id,
                suggestion,
                "ai_draft",
            )

        self.db.record_action(
            post_id,
            "COMMENT_DRAFT",
            "PENDING_APPROVAL",
            "ai_pipeline",
        )

        notification = self._format_notification(
            post,
            rec,
        )

        telegram.notify(notification)

        if self.settings.desktop_notifications:
            desktop.notify(
                "LinkedIn AI Engagement Agent",
                notification,
            )

        self._human_review(
            post,
            rec,
        )

    def _format_notification(self, post: dict, rec: dict) -> str:
        lines = [
            "LinkedIn AI Engagement Assistant",
            "",
            f"Author: {post.get('author', 'Unknown')}",
            f"Topic: {rec['topic']}",
            f"Relevance: {rec['relevance']}%",
            f"Recommendation: {rec['recommended_action']}",
            f"Reason: {rec['reason']}",
        ]

        for i, suggestion in enumerate(
            rec["comment_suggestions"],
            1,
        ):
            lines.append(
                f"Option {i}: {suggestion}"
            )

        if post.get("url"):
            lines.append(
                f"Open post: {post['url']}"
            )

        lines.append(
            "No LinkedIn action is performed automatically in this mode."
        )

        return "\n".join(lines)

    def _human_review(self, post: dict, rec: dict):
        print(
            f"\n--- {post.get('author', 'Unknown')} ---"
        )
        print(
            f"Topic: {rec['topic']} | "
            f"Relevance: {rec['relevance']}%"
        )
        print(
            f"Recommendation: {rec['recommended_action']}"
        )
        print(
            f"Reason: {rec['reason']}"
        )

        for i, suggestion in enumerate(
            rec["comment_suggestions"],
            1,
        ):
            print(
                f"  {i}. {suggestion}"
            )

        if post.get("url"):
            print(
                f"  Open: {post['url']}"
            )

        try:
            choice = input(
                "[1] Copy suggestion / [S]kip > "
            ).strip().lower()
        except EOFError:
            choice = "s"

        if (
            choice == "1"
            and rec["comment_suggestions"]
        ):
            comment = rec["comment_suggestions"][0]

            decision = self.guard.check_action(
                "COMMENT",
                requires_manual_approval=True,
                approved=True,
                comment_text=comment,
            )

            if (
                decision["allowed"]
                and self.settings.api_automation_allowed
            ):
                from linkedin.official_api import (
                    OfficialLinkedInAPI,
                )

                result = OfficialLinkedInAPI(
                    self.guard
                ).create_comment(
                    post.get(
                        "urn",
                        post.get("id", ""),
                    ),
                    comment,
                    approved=True,
                )

                status = (
                    "EXECUTED"
                    if result["allowed"]
                    else "BLOCKED"
                )

                self.db.record_action(
                    post["id"],
                    "COMMENT",
                    status,
                    "official_api",
                )

                print(
                    result["reason"]
                )

            else:
                self.db.record_action(
                    post["id"],
                    "COMMENT",
                    "MANUAL_BY_HUMAN",
                    "human",
                )

                print(
                    "\nCopy this comment and post it manually:"
                )
                print(comment)

        else:
            self.db.record_action(
                post["id"],
                "SKIP",
                "SKIPPED",
                "human",
            )

            print("Skipped.")

    def run(self, once=False):
        self.start_session()

        outcome = "STOPPED"

        # SAFE_DEMO is intentionally repeatable so the demo
        # can be run multiple times without modifying the database.
        force_demo = (
            once
            and self.settings.mode == "SAFE_DEMO"
        )

        try:
            while not STOP_FILE.exists():
                posts = self.discovery.discover(
                    self.settings.mode
                )

                if not posts:
                    print(
                        "No posts available for this cycle."
                    )
                    logger.info(
                        "No posts available for this cycle."
                    )

                for post in posts:
                    if STOP_FILE.exists():
                        break

                    self.process_post(
                        post,
                        force_demo=force_demo,
                    )

                if once:
                    break

                time.sleep(60)

            outcome = (
                "STOPPED_BY_COMMAND"
                if STOP_FILE.exists()
                else "COMPLETED"
            )

        except SafetyEvent as exc:
            print(
                "\n!!! SAFETY EVENT !!!"
            )
            print(
                "Agent stopped. "
                "No further LinkedIn action will be attempted."
            )
            print(
                f"Detail: {exc}"
            )
            outcome = "SAFETY_EVENT"

        except KeyboardInterrupt:
            print(
                "\nEmergency shutdown. Agent stopped."
            )

            STOP_FILE.write_text(
                "ctrl-c",
                encoding="utf-8",
            )

            outcome = "CTRL_C"

        finally:
            self.end_session(outcome)
            self.db.close()