"""Deterministic offline fallback. No network and no secrets."""
from __future__ import annotations

KEYWORDS = {
    "AI": {"ai", "artificial intelligence", "machine learning", "llm", "inference", "model", "genai"},
    "Software": {"software", "python", "javascript", "api", "backend", "frontend", "github", "developer"},
    "Cloud": {"cloud", "aws", "azure", "gcp", "kubernetes", "docker", "devops"},
    "Business": {"startup", "business", "revenue", "customer", "growth", "marketing"},
}


def heuristic_analysis(text: str, interests: list[str]) -> dict:
    lower = text.lower()
    matched = []
    for topic, words in KEYWORDS.items():
        if any(word in lower for word in words):
            matched.append(topic)

    interest_hits = sum(1 for item in interests if item.lower() in lower)
    base = min(100, len(matched) * 18 + interest_hits * 12)

    professional = min(100, base + (20 if len(text) > 100 else 0))
    technical = min(100, base + (15 if any(x in lower for x in ("api", "code", "kubernetes", "model", "inference")) else 0))
    business = min(100, base + (15 if any(x in lower for x in ("startup", "revenue", "customer", "growth")) else 0))

    topic = matched[0] if matched else "General"
    worth = base >= 45

    comments = []
    if worth:
        comments = [
            f"The practical details around {topic.lower()} are especially useful. What trade-off mattered most during implementation?",
            f"Interesting perspective on {topic.lower()}. Which metric did you use to validate the improvement?",
        ]

    return {
        "topic": topic,
        "relevance": base,
        "professional_value": professional,
        "networking_value": min(100, base + 10),
        "technical_relevance": technical,
        "business_relevance": business,
        "reason": (
            f"Matched interests/topics: {', '.join(matched) if matched else 'none'}."
        ),
        "worth_commenting": worth,
        "comment_options": comments,
    }
