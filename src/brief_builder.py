from __future__ import annotations

from typing import Any


def build_brief(meeting: dict[str, Any], classification: dict[str, Any]) -> dict[str, Any]:
    agenda = meeting.get("agenda") or []
    questions = meeting.get("open_questions") or []
    notes = meeting.get("context_notes") or []
    return {
        "meeting_id": meeting.get("id"),
        "title": f"Brief: {meeting.get('title')}",
        "draft_only": True,
        "readiness": classification.get("category"),
        "agenda": agenda,
        "open_questions": questions,
        "context_notes": notes,
        "next_step": classification.get("recommended_action"),
    }
