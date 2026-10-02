"""OpenAI-compatible LLM client. Only post content and configured interests are sent."""
from __future__ import annotations

import json
import re

import config
from ai import prompts


class LLMClient:
    def __init__(self):
        self.key = config.SETTINGS.ai_api_key
        self.base_url = config.SETTINGS.ai_base_url
        self.model = config.SETTINGS.ai_model

    @property
    def available(self) -> bool:
        return bool(self.key)

    def analyze_post(self, post_text: str) -> dict | None:
        if not self.available:
            return None

        try:
            import requests

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "response_format": {"type": "json_object"},
                    "messages": [
                        {"role": "system", "content": prompts.SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": prompts.ANALYSIS_PROMPT.format(
                                interests=", ".join(config.SETTINGS.user_interests),
                                post_text=post_text[:4000],
                            ),
                        },
                    ],
                    "temperature": 0.3,
                },
                timeout=30,
            )
            if response.status_code != 200:
                return None

            content = response.json()["choices"][0]["message"]["content"]
            return self._extract_json(content)
        except Exception:
            return None

    @staticmethod
    def _extract_json(text: str) -> dict | None:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
