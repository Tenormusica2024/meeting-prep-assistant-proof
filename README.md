# Meeting Prep Assistant Proof

A public-safe proof slice for an AI secretary that turns sample meeting inputs into a pre-meeting brief without sending messages, editing calendars, or using private notes.

## One-minute summary

This repository demonstrates a practical AI-secretary pattern:

```text
sample meetings -> readiness triage -> meeting brief -> human confirmation queue
```

It is meant as a reusable proof for:

- pre-meeting preparation
- agenda and context readiness checks
- human-in-the-loop automation
- safe action boundaries before external side effects
- deterministic Python implementation with synthetic fixtures and tests

## For reviewers

Review these first:

1. `outputs/meeting_prep_report.md` — generated sample report
2. `src/meeting_prep.py` — classification logic without external side effects
3. `tests/` — safety and behavior checks
4. `docs/privacy-boundary.md` — what must not be published
5. `docs/showcase-copy.md` — how to describe this proof in public demo contexts

## What this proves

This proof shows that an AI secretary can help with meeting preparation without directly contacting participants or changing calendar events. It can first:

- classify meetings into ready, needs-agenda, needs-context, needs-confirmation, and send-later groups
- explain what is missing before the meeting
- create a compact pre-meeting brief from sample agenda, questions, and notes
- place attendee-send or calendar-update suggestions into a confirmation queue
- keep the default demo sample-first, deterministic, and public-safe

## Scope boundaries

This is not:

- a production meeting assistant
- a live calendar, email, chat, or document integration
- an autonomous meeting-note sender
- a hosted SaaS demo

It is a focused proof of the meeting preparation and confirmation pattern.

## Quick demo

From this proof directory:

```powershell
python -X utf8 run_demo.py
```

Run tests:

```powershell
python -m pytest tests -q
python scripts/check_public_boundary.py
```

## Safety model

The default mode is:

- no external APIs
- no participant messages
- no calendar updates
- no document sharing
- no automatic action execution
- no OAuth requirement for the demo

Action-worthy recommendations are represented as confirmation queue entries for human review.

## Public/private boundary

This repository uses synthetic fixtures only. It should not contain real meeting notes, real participant names, meeting links, customer details, local absolute paths, tokens, secrets, credentials, or private knowledge-base outputs.

See:

- `docs/privacy-boundary.md`
- `docs/public-export-checklist.md`
- `docs/showcase-copy.md`
