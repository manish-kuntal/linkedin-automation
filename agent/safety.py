"""Central fail-closed safety gate."""
from __future__ import annotations

import time
from datetime import datetime, timezone

from config import SETTINGS, STOP_FILE, LOG_DIR


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


class SafetyEvent(Exception):
    pass


class SafetyGuard:
    def __init__(self, db=None):
        self.db = db
        self.security_log = LOG_DIR / "security.log"
        self._daily_counts = {}
        self._last_action_ts = 0.0
        self._seen_comment_hashes = set()

    def log_security(self, event: str, detail: str = ""):
        with open(self.security_log, "a", encoding="utf-8") as f:
            f.write(f"{_now()} {event} {detail}\n")

    def raise_safety_event(self, event_type: str, detail: str = ""):
        STOP_FILE.write_text("safety_event", encoding="utf-8")
        if self.db:
            self.db.record_safety_event(event_type, detail)
        self.log_security(f"SAFETY_EVENT {event_type}", detail)
        raise SafetyEvent(f"{event_type}: {detail}")

    def handle_api_response(self, status_code: int, body: str = ""):
        if status_code in (401, 403):
            self.raise_safety_event("AUTH_FAILURE", f"HTTP {status_code}")
        if status_code == 429:
            self.raise_safety_event("RATE_LIMIT", "HTTP 429")
        if status_code >= 500 or status_code not in (200, 201, 202, 204):
            self.raise_safety_event("UNEXPECTED_RESPONSE", f"HTTP {status_code} {body[:200]}")

    def check_action(
        self,
        action: str,
        requires_manual_approval: bool = True,
        approved: bool = False,
        comment_text: str = "",
    ) -> dict:
        try:
            if STOP_FILE.exists():
                return self._block("Emergency stop active.")

            allowed_actions = {"LIKE", "COMMENT", "SHARE", "NOTIFY", "ANALYZE", "OPEN"}
            if action not in allowed_actions:
                return self._block(f"Unknown action '{action}'.")

            if action in {"ANALYZE", "NOTIFY", "OPEN"}:
                return {"allowed": True, "reason": "Assistive action; no account state change."}

            if not SETTINGS.api_automation_allowed:
                return self._block(
                    "Official API automation is not enabled and approved. "
                    "Perform the interaction manually."
                )

            if requires_manual_approval and not approved:
                return self._block("Manual approval required.")

            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            counts = self._daily_counts.setdefault(
                today, {"LIKE": 0, "COMMENT": 0, "SHARE": 0}
            )
            limit = (
                SETTINGS.max_comments_per_day
                if action == "COMMENT"
                else SETTINGS.max_actions_per_day
            )
            if counts[action] >= limit:
                return self._block("Daily limit reached.")

            if counts[action] and time.time() - self._last_action_ts < SETTINGS.cooldown_seconds:
                return self._block("Cooldown active.")

            if action == "COMMENT":
                digest = hash(comment_text.strip().lower())
                if digest in self._seen_comment_hashes:
                    return self._block("Duplicate comment detected.")
                self._seen_comment_hashes.add(digest)

            counts[action] += 1
            self._last_action_ts = time.time()
            self.log_security("ACTION_ALLOWED", action)
            return {"allowed": True, "reason": "All safety checks passed."}
        except Exception as exc:
            self.log_security("GUARD_ERROR", str(exc))
            return self._block(f"Guard error; fail-closed: {exc}")

    @staticmethod
    def _block(reason: str) -> dict:
        return {"allowed": False, "reason": reason}
