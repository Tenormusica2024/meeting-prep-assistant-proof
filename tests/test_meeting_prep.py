from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from meeting_prep import build_report, classify_meeting, load_json  # noqa: E402


def rules():
    return load_json(ROOT / "samples" / "prep_rules.json")


def test_confirmation_takes_priority_over_readiness():
    meeting = {
        "id": "x",
        "title": "Needs approval",
        "starts_in_hours": 2,
        "agenda": ["Discuss"],
        "context_notes": ["Ready"],
        "open_questions": [],
        "needs_send_to_participants": True,
        "needs_calendar_update": False,
        "requires_confirmation": False,
    }

    result = classify_meeting(meeting, rules())

    assert result["category"] == "needs_confirmation"
    assert result["requires_external_action"] is True


def test_classifies_expected_categories():
    meetings = load_json(ROOT / "samples" / "meetings.json")
    report = build_report(meetings, rules())
    categories = {row["classification"]["category"] for row in report["items"]}

    assert {"ready", "needs_agenda", "needs_confirmation", "send_later"}.issubset(categories)
    assert report["summary"]["brief_count"] == 5
    assert report["summary"]["confirmation_queue_count"] == 2


def test_confirmation_queue_has_no_executed_side_effects():
    report = build_report(load_json(ROOT / "samples" / "meetings.json"), rules())

    assert report["confirmation_queue"]
    assert all(item["side_effect_status"] == "not_executed" for item in report["confirmation_queue"])
    assert all(item["requires_human_review"] is True for item in report["confirmation_queue"])
