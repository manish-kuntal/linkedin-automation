"""Post analyzer. Uses LLM when configured; otherwise deterministic local scoring."""
from __future__ import annotations

from ai.llm import LLMClient
from ai.scoring import heuristic_analysis


class Analyzer:
    def __init__(self, settings):
        self.settings = settings
        self.llm = LLMClient()

    def analyze(self, post_text: str) -> dict:
        text = (post_text or "").strip()
        if not text:
            return {
                "topic": "unknown",
                "relevance": 0,
                "professional_value": 0,
                "networking_value": 0,
                "technical_relevance": 0,
                "business_relevance": 0,
                "reason": "Empty post.",
                "worth_commenting": False,
                "comment_options": [],
            }

        result = self.llm.analyze_post(text)
        return result if result is not None else heuristic_analysis(text, self.settings.user_interests)
