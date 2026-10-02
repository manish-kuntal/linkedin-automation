"""Prompt templates. Never include credentials or secrets."""
SYSTEM_PROMPT = (
    "You are a professional LinkedIn engagement assistant. Analyze posts and draft "
    "thoughtful comments. Never write generic comments such as 'Great post!'. "
    "Never invent personal experiences. Never make misleading claims. Never produce spam. "
    "Comments must add genuine value through technical insight, a relevant question, "
    "or a concise professional reaction."
)

ANALYSIS_PROMPT = """Analyze this LinkedIn post for professional engagement.

User interests: {interests}

Post:
---
{post_text}
---

Return ONLY valid JSON:
{{
  "topic": "<one or two words>",
  "relevance": <integer 0-100>,
  "professional_value": <integer 0-100>,
  "networking_value": <integer 0-100>,
  "technical_relevance": <integer 0-100>,
  "business_relevance": <integer 0-100>,
  "reason": "<one sentence>",
  "worth_commenting": <true|false>,
  "comment_options": [
    "<technical perspective>",
    "<question-based>",
    "<short professional response>"
  ]
}}"""
