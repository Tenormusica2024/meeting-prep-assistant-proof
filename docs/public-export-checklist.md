# Public Export Checklist

Before publishing or updating this proof, confirm:

- [ ] The repository contains synthetic samples only.
- [ ] No real meeting notes, participant names, contact details, or meeting links are present.
- [ ] No tokens, secrets, credentials, or local absolute paths are present.
- [ ] `python -m pytest tests -q` passes.
- [ ] `python scripts/check_public_boundary.py` passes.
- [ ] The README states the no-participant-send and no-calendar-update boundaries.
- [ ] Generated outputs are deterministic and safe to show.
- [ ] External actions are represented only as confirmation queue items.

Optional future integrations may document setup steps, but the default proof should remain sample-first and should not require OAuth.
