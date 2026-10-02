import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from agent.analyzer import Analyzer
from agent.recommender import Recommender
from agent.safety import SafetyGuard
from storage.database import Database


def test_analysis():
    result = Analyzer(config.SETTINGS).analyze(
        "Local AI deployment cut our latency by 40%."
    )
    assert 0 <= result["relevance"] <= 100
    assert result["topic"]


def test_recommendation():
    result = Recommender(config.SETTINGS).recommend({
        "relevance": 91,
        "topic": "AI",
        "worth_commenting": True,
        "professional_value": 80,
        "comment_options": [],
    })
    assert result["recommended_action"] in {"REVIEW", "MAYBE", "SKIP"}
    assert len(result["comment_suggestions"]) <= 3


def test_generic_comments_blocked():
    result = Recommender(config.SETTINGS).recommend({
        "relevance": 90,
        "professional_value": 70,
        "worth_commenting": True,
        "comment_options": [
            "Great post!",
            "x",
            "This is a solid breakdown of the trade-offs in local inference deployment.",
        ],
    })
    assert all(x.lower() != "great post!" for x in result["comment_suggestions"])
    assert len(result["comment_suggestions"]) == 1


def test_safety_blocks_external_action_by_default(tmp_path):
    db = Database()
    guard = SafetyGuard(db)
    config.STOP_FILE.unlink(missing_ok=True)
    result = guard.check_action("LIKE", requires_manual_approval=True, approved=True)
    assert result["allowed"] is False
    db.close()


def test_emergency_stop():
    config.STOP_FILE.write_text("test", encoding="utf-8")
    db = Database()
    guard = SafetyGuard(db)
    result = guard.check_action("LIKE", approved=True)
    assert result["allowed"] is False
    config.STOP_FILE.unlink(missing_ok=True)
    db.close()


def test_unknown_action_blocks():
    db = Database()
    guard = SafetyGuard(db)
    config.STOP_FILE.unlink(missing_ok=True)
    result = guard.check_action("DELETE_ACCOUNT", approved=True)
    assert result["allowed"] is False
    db.close()
