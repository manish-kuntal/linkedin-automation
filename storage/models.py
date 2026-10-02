"""Shared dataclasses."""
from dataclasses import dataclass, field
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Post:
    id: str
    author: str
    url: str = ""
    text: str = ""
    source: str = "mock"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data.get("id", "")),
            author=data.get("author", "Unknown"),
            url=data.get("url", ""),
            text=data.get("text", ""),
            source=data.get("source", "mock"),
        )


@dataclass
class Analysis:
    relevance: int = 0
    topic: str = "unknown"
    recommended_action: str = "SKIP"
    reason: str = ""
    comment_suggestions: list = field(default_factory=list)

    def to_dict(self):
        return self.__dict__.copy()


@dataclass
class Action:
    post_id: str
    action: str
    status: str = "PENDING_APPROVAL"
    source: str = "mock"
    timestamp: str = field(default_factory=now)

    def to_dict(self):
        return self.__dict__.copy()
