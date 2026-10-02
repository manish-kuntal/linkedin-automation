"""Recommendation layer. It never performs LinkedIn actions."""
GENERIC_BANNED = (
    "great post", "nice post", "awesome", "well said", "love this",
    "amazing", "congrats", "thanks for sharing",
)


class Recommender:
    def __init__(self, settings):
        self.settings = settings

    def recommend(self, analysis: dict) -> dict:
        relevance = int(analysis.get("relevance", 0))
        worth = bool(analysis.get("worth_commenting", False))
        value = int(analysis.get("professional_value", 0))

        if relevance >= 70 and (worth or value >= 60):
            action = "REVIEW"
        elif relevance >= 40:
            action = "MAYBE"
        else:
            action = "SKIP"

        suggestions = []
        for suggestion in analysis.get("comment_options", []):
            text = str(suggestion).strip()
            if not text or len(text) < 15:
                continue
            lower = text.lower()
            if any(lower.startswith(b) or lower == b for b in GENERIC_BANNED):
                continue
            if text not in suggestions:
                suggestions.append(text)

        return {
            "relevance": max(0, min(100, relevance)),
            "topic": analysis.get("topic", "unknown"),
            "recommended_action": action,
            "reason": analysis.get("reason", ""),
            "comment_suggestions": suggestions[: self.settings.max_suggestions],
        }
