# AGENTS.md

# Avatra — Instructions for AI Coding Agents

This file is for AI agents operating on the repository.

It complements `CLAUDE.md`.

## General behavior

Be conservative.

Do not rewrite the project unless explicitly asked.

Prefer a minimal, correct implementation over an ambitious one.

When uncertain, preserve existing behavior and document the uncertainty.

## Required reading before work

Always read:

1. `CLAUDE.md`
2. this file
3. the relevant docs under `docs/`
4. the existing implementation files related to the task

## How to make changes

1. Identify the affected domain concept.
2. Locate existing models, services, routes and UI pieces.
3. Reuse existing patterns.
4. Add tests or at least keep the code testable.
5. Update documentation.
6. Provide a concise final summary.

## Never do this without explicit approval

- Replace FastAPI with another backend framework.
- Replace SQLite as the default database.
- Turn Kodi metadata scraping into Avatra's core feature.
- Require a paid API for normal operation.
- Require cloud authentication for local use.
- Move business logic into frontend JavaScript.
- Remove manual fallback workflows.
- Break existing routes without migration notes.
- Rename the project.

## Commit style

Suggested commit messages:

```text
feat(media): add physical edition status
fix(barcode): handle unknown barcode gracefully
docs(kodi): document mapping strategy
refactor(api): extract loan service
test(location): cover loan return workflow
```

## Preferred task flow

For feature work:

1. Explain intended implementation.
2. Modify backend models/services.
3. Modify API.
4. Modify frontend only after backend behavior is stable.
5. Add or update tests.
6. Update docs.

For bug fixes:

1. Reproduce or reason about the bug.
2. Add a regression test when possible.
3. Fix the smallest affected area.
4. Explain the root cause.

For refactors:

1. Preserve behavior.
2. Avoid mixing refactor and feature work.
3. Keep diffs reviewable.

## Communication style

When reporting work, include:

- files changed;
- behavior changed;
- tests/checks run;
- risks or follow-up items.

Do not claim that tests passed unless they were actually run.
