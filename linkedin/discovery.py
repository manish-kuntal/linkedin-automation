"""Safe content discovery. No LinkedIn scraping or browser automation."""
from __future__ import annotations
import json
from pathlib import Path

MOCK_FILE = Path(__file__).resolve().parent.parent / "tests" / "mock_posts.json"
MANUAL_FILE = Path(__file__).resolve().parent.parent / "manual_posts.json"


def load_mock_posts() -> list[dict]:
    if not MOCK_FILE.exists():
        return []
    with MOCK_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


class Discovery:
    def __init__(self, settings):
        self.settings = settings

    def discover(self, mode: str) -> list[dict]:
        if mode == "SAFE_DEMO":
            return load_mock_posts()
        if mode == "LINKEDIN_ASSISTANT":
            if not MANUAL_FILE.exists():
                return []
            try:
                return json.loads(MANUAL_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return []
        # Official API discovery is intentionally not implemented here.
        # It must only be added against an explicitly authorized LinkedIn API.
        return []
