from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from brief_builder import build_brief
from confirmation_queue import build_confirmation_item


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _number(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def classify_meeting(meeting: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    agenda = meeting.get("agenda") or []
    notes = meeting.get("context_notes") or []
    questions = meeting.get("open_questions") or []
    starts_in_hours = _number(meeting.get("starts_in_hours"), 999)
    requires_confirmation = _bool(meeting.get("requires_confirmation"))
    needs_send = _bool(meeting.get("needs_send_to_participants"))
    needs_calendar_update = _bool(meeting.get("needs_calendar_update"))

    if requires_confirmation or needs_send or needs_calendar_update:
        return {
            "category": "needs_confirmation",
            "severity": "review",
            "reason": "participant send or calendar change requires human confirmation",
            "recommended_action": "review_brief_before_external_action",
            "requires_external_action": True,
        }

    if not agenda:
        return {
            "category": "needs_agenda",
            "severity": "medium",
            "reason": "agenda is missing",
            "recommended_action": "add_agenda_before_meeting",
            "requires_external_action": False,
        }

    if not notes and questions:
        return {
            "category": "needs_context",
            "severity": "medium",
            "reason": "open questions exist but context notes are missing",
            "recommended_action": "collect_context_before_meeting",
            "requires_external_action": False,
        }

    if starts_in_hours > _number(rules.get("send_later_hours_threshold"), 48):
        return {
            "category": "send_later",
            "severity": "low",
            "reason": "meeting is not close enough for final preparation",
            "recommended_action": "revisit_closer_to_meeting",
            "requires_external_action": False,
        }

    return {
        "category": "ready",
        "severity": "normal" if starts_in_hours <= _number(rules.get("soon_hours_threshold"), 24) else "low",
        "reason": "agenda and context are ready for a draft brief",
        "recommended_action": "use_brief_for_human_review",
        "requires_external_action": False,
    }


def build_report(meetings: list[dict[str, Any]], rules: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    queue: list[dict[str, Any]] = []
    briefs: list[dict[str, Any]] = []

    for meeting in meetings:
        classification = classify_meeting(meeting, rules)
        brief = build_brief(meeting, classification)
        briefs.append(brief)
        rows.append({
            "meeting": {
                "id": meeting.get("id"),
                "title": meeting.get("title"),
                "meeting_type": meeting.get("meeting_type"),
                "starts_in_hours": meeting.get("starts_in_hours"),
            },
            "classification": classification,
            "brief": brief,
        })
        if classification.get("requires_external_action"):
            queue.append(build_confirmation_item(meeting, classification, brief))

    counts: dict[str, int] = {}
    for row in rows:
        cat = row["classification"]["category"]
        counts[cat] = counts.get(cat, 0) + 1

    return {
        "summary": {
            "meetings_scanned": len(meetings),
            "counts": counts,
            "brief_count": len(briefs),
            "confirmation_queue_count": len(queue),
            "safety": rules.get("safety", "sample-first / no-participant-send / no-calendar-update"),
        },
        "items": rows,
        "briefs": briefs,
        "confirmation_queue": queue,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Meeting Prep Assistant Proof Report",
        "",
        f"- scanned: `{report['summary']['meetings_scanned']}`",
        f"- safety: `{report['summary']['safety']}`",
        f"- meeting briefs: `{report['summary']['brief_count']}`",
        f"- confirmation queue: `{report['summary']['confirmation_queue_count']}`",
        "",
        "## Reviewer Highlights",
        "",
        "- Meetings are checked before participant send or calendar update.",
        "- Briefs are draft-only and generated from synthetic fixtures.",
        "- Missing agenda/context is surfaced before the meeting.",
        "- External actions are represented as confirmation queue entries.",
        "",
        "## Items",
        "",
    ]
    for row in report["items"]:
        meeting = row["meeting"]
        cls = row["classification"]
        brief = row["brief"]
        lines.extend([
            f"### {meeting.get('title')}",
            f"- type: `{meeting.get('meeting_type')}` / starts_in_hours: `{meeting.get('starts_in_hours')}`",
            f"- category: `{cls.get('category')}` / severity: `{cls.get('severity')}`",
            f"- reason: {cls.get('reason')}",
            f"- recommended_action: `{cls.get('recommended_action')}`",
            f"- agenda_items: `{len(brief.get('agenda') or [])}` / open_questions: `{len(brief.get('open_questions') or [])}`",
            "",
        ])

    lines.extend(["## Confirmation Queue", ""])
    for item in report["confirmation_queue"]:
        lines.append(f"- `{item['id']}` {item['title']} -> `{item['recommended_action']}`")
    if not report["confirmation_queue"]:
        lines.append("- none")

    lines.extend(["", "## Draft Briefs", ""])
    for brief in report["briefs"]:
        lines.extend([
            f"### meeting `{brief['meeting_id']}`",
            f"- draft_only: `{brief['draft_only']}`",
            f"- readiness: `{brief['readiness']}`",
            f"- next_step: `{brief['next_step']}`",
            "",
        ])
    if not report["briefs"]:
        lines.append("- none")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample-first meeting prep assistant proof")
    parser.add_argument("--meetings", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args(argv)

    report = build_report(load_json(args.meetings), load_json(args.rules))
    out = Path(args.out)
    json_out = Path(args.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(report), encoding="utf-8", newline="\n")
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out}")
    print(f"wrote {json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
