# Meeting Prep Assistant Proof Report

- scanned: `5`
- safety: `sample-first / no-participant-send / no-calendar-update / confirmation-required`
- meeting briefs: `5`
- confirmation queue: `2`

## Reviewer Highlights

- Meetings are checked before participant send or calendar update.
- Briefs are draft-only and generated from synthetic fixtures.
- Missing agenda/context is surfaced before the meeting.
- External actions are represented as confirmation queue entries.

## Items

### Implementation planning sync
- type: `planning` / starts_in_hours: `3`
- category: `ready` / severity: `normal`
- reason: agenda and context are ready for a draft brief
- recommended_action: `use_brief_for_human_review`
- agenda_items: `3` / open_questions: `1`

### Requirements clarification
- type: `requirements` / starts_in_hours: `5`
- category: `needs_agenda` / severity: `medium`
- reason: agenda is missing
- recommended_action: `add_agenda_before_meeting`
- agenda_items: `0` / open_questions: `2`

### Review packet handoff
- type: `review` / starts_in_hours: `8`
- category: `needs_confirmation` / severity: `review`
- reason: participant send or calendar change requires human confirmation
- recommended_action: `review_brief_before_external_action`
- agenda_items: `2` / open_questions: `0`

### Weekly optional check-in
- type: `checkin` / starts_in_hours: `72`
- category: `send_later` / severity: `low`
- reason: meeting is not close enough for final preparation
- recommended_action: `revisit_closer_to_meeting`
- agenda_items: `1` / open_questions: `0`

### Schedule conflict review
- type: `scheduling` / starts_in_hours: `2`
- category: `needs_confirmation` / severity: `review`
- reason: participant send or calendar change requires human confirmation
- recommended_action: `review_brief_before_external_action`
- agenda_items: `1` / open_questions: `1`

## Confirmation Queue

- `confirm-mtg-003` Review packet handoff -> `review_brief_before_external_action`
- `confirm-mtg-005` Schedule conflict review -> `review_brief_before_external_action`

## Draft Briefs

### meeting `mtg-001`
- draft_only: `True`
- readiness: `ready`
- next_step: `use_brief_for_human_review`

### meeting `mtg-002`
- draft_only: `True`
- readiness: `needs_agenda`
- next_step: `add_agenda_before_meeting`

### meeting `mtg-003`
- draft_only: `True`
- readiness: `needs_confirmation`
- next_step: `review_brief_before_external_action`

### meeting `mtg-004`
- draft_only: `True`
- readiness: `send_later`
- next_step: `revisit_closer_to_meeting`

### meeting `mtg-005`
- draft_only: `True`
- readiness: `needs_confirmation`
- next_step: `review_brief_before_external_action`
