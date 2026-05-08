from __future__ import annotations

from typing import Any


def build_confirmation_item(meeting: dict[str, Any], classification: dict[str, Any], brief: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"confirm-{meeting.get('id')}",
        "title": meeting.get("title"),
        "meeting_id": meeting.get("id"),
        "recommended_action": classification.get("recommended_action"),
        "reason": classification.get("reason"),
        "brief_title": brief.get("title"),
        "side_effect_status": "not_executed",
        "requires_human_review": True,
    }
