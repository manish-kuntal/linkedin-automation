"""Official LinkedIn API client.

This module is intentionally fail-closed. It is NOT browser automation and
must only be used when the application has the required official approval.
"""
from __future__ import annotations

import requests

from agent.safety import SafetyGuard
from config import SETTINGS


class LinkedInAPIError(Exception):
    pass


class OfficialLinkedInAPI:
    BASE = "https://api.linkedin.com"

    def __init__(self, guard: SafetyGuard):
        self.guard = guard
        self.token = SETTINGS.linkedin_access_token

    @property
    def automation_enabled(self):
        return SETTINGS.api_automation_allowed and bool(self.token)

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202601",
            "Content-Type": "application/json",
        }

    def react_to_post(self, post_urn: str, approved=False) -> dict:
        decision = self.guard.check_action(
            "LIKE", requires_manual_approval=True, approved=approved
        )
        if not decision["allowed"]:
            return decision
        if not self.automation_enabled:
            return {"allowed": False, "reason": "Official API is not enabled and approved."}

        # Endpoint/payload must be validated against LinkedIn's current official
        # documentation before enabling production use.
        return {
            "allowed": False,
            "reason": "Reaction execution is intentionally disabled until the exact current LinkedIn API permission/endpoint is verified.",
        }

    def create_comment(self, post_urn: str, text: str, approved=False) -> dict:
        decision = self.guard.check_action(
            "COMMENT",
            requires_manual_approval=True,
            approved=approved,
            comment_text=text,
        )
        if not decision["allowed"]:
            return decision
        if not self.automation_enabled:
            return {"allowed": False, "reason": "Official API is not enabled and approved."}

        return {
            "allowed": False,
            "reason": "Comment execution is intentionally disabled until the exact current LinkedIn API permission/endpoint is verified.",
        }
