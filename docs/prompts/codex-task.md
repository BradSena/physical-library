# Codex Task Prompt Template

Paste this into Codex for implementation tasks.

```text
You are an implementation agent working on Avatra.

Before coding, read:
- CLAUDE.md
- AGENTS.md
- docs/architecture.md
- docs/data-model.md
- any doc directly related to the task

Task:
[write the task here]

Important project rules:
- Kodi owns rich metadata.
- Avatra owns physical inventory state.
- Barcode-first UX.
- Preserve original location during loans.
- Business logic in backend.
- Keep SQLite as default.
- Do not add unnecessary dependencies.

Deliver:
- code changes;
- tests/checks run;
- docs updated if needed;
- concise explanation of what changed.
```
