# Privacy Boundary

This repository is designed to be public-safe by default.

## Allowed

- Synthetic meeting records
- Generic role labels instead of real participant names
- Generic agenda, open question, and context-note samples
- Deterministic sample outputs
- Local-only Python logic
- Documentation about the no-send and no-calendar-update safety model

## Not allowed

- Real meeting notes or transcripts
- Real participant names, contact details, or meeting links
- Real customer, vendor, or employer data
- OAuth tokens, API keys, secrets, credentials, or refresh tokens
- Local absolute paths
- Private knowledge-base outputs
- Internal project names that are not meant for public demonstration

## Default behavior

The demo does not connect to calendar, email, chat, document, or meeting systems. It reads sample JSON files and writes local report files only.

Any item that would require participant send, document sharing, or calendar update is represented as a confirmation queue entry for human review.
