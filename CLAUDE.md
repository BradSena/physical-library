# CLAUDE.md

# Avatra — AI Development Constitution

> Canonical project instructions for Claude Code, OpenAI Codex, Gemini CLI,
> Copilot agents, and any other AI development assistant working on this repo.

Avatra is a self-hosted application for managing a physical media collection and
bridging it with a home-cinema automation environment.

This file is intentionally high-level. Detailed rules live in `docs/`.

## 1. Project mission

Avatra manages the **physical reality** of a media collection:

- which physical items exist;
- where they are stored;
- whether they are available, loaned, displayed, missing, or digitized;
- how they relate to Kodi items;
- how they can trigger home-cinema workflows.

Avatra does **not** replace Kodi.

Kodi remains responsible for rich media metadata such as posters, synopses,
actors, ratings, collections, fan art and playback library presentation.

Avatra exists because a user with hundreds of physical discs needs a practical
way to scan, locate, browse, loan, reserve and launch media without turning the
project into a full media-center replacement.

## 2. Absolute rules

These rules must not be violated unless the user explicitly asks for a change in
project direction.

1. **Kodi is the metadata source of truth.**
   Do not build a competing full movie metadata scraper.

2. **Avatra owns physical inventory state.**
   Location, loans, availability and physical edition details belong to Avatra.

3. **Barcode first.**
   Adding a physical item must start with barcode scanning whenever possible.

4. **Manual entry is fallback, not the main workflow.**

5. **Home Assistant is an integration/host, not the business logic core.**

6. **Business logic belongs in the backend.**
   The frontend should not become the domain engine.

7. **Offline/self-hosted operation is preferred.**
   Avoid mandatory cloud dependencies.

8. **Do not impose rigid shelf slot logic.**
   Locations must stay flexible.

9. **A loan never erases the original location.**

10. **Keep it simple for a non-developer user.**

## 3. Repository structure

Expected structure:

```text
avatra/
├── CLAUDE.md
├── AGENTS.md
├── README.md
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── avatra.db
├── frontend/
├── kodi-addon/
├── homeassistant-addon/
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── api.md
│   ├── backend.md
│   ├── frontend.md
│   ├── barcode.md
│   ├── kodi.md
│   ├── homeassistant.md
│   ├── ui-ux.md
│   ├── coding-style.md
│   ├── testing.md
│   ├── roadmap.md
│   ├── decisions/
│   └── prompts/
└── scripts/
```

If the real repository differs, adapt carefully without breaking existing code.

## 4. Current technical stack

Backend:

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

Frontend:

- static HTML/CSS/JavaScript for now;
- responsive/mobile-first;
- future Home Assistant-friendly UI.

Integrations:

- Kodi add-on;
- Home Assistant add-on;
- future automation hooks.

## 5. Domain summary

Core domain objects:

- `MediaItem`
- `PhysicalEdition`
- `Barcode`
- `Location`
- `Loan`
- `Holder`
- `KodiMapping`
- `InventoryEvent`
- `Settings`

The exact model is described in `docs/data-model.md`.

## 6. Development style

Prefer:

- small changes;
- readable code;
- explicit domain rules;
- simple API contracts;
- tests for business rules;
- documentation updates with every meaningful feature.

Avoid:

- large speculative refactors;
- unnecessary dependencies;
- hidden business logic in UI code;
- mandatory cloud services;
- changing API contracts without documenting it.

## 7. AI agent workflow

Before modifying code:

1. Read this file.
2. Read `AGENTS.md`.
3. Read the relevant files in `docs/`.
4. Inspect existing code before creating new patterns.
5. Make the smallest coherent change.
6. Run available tests/checks.
7. Update docs if behavior changes.
8. Summarize the diff clearly.

## 8. Definition of done

A task is complete only when:

- code compiles/runs locally according to available commands;
- relevant tests are added or updated;
- API behavior is documented if changed;
- user-facing behavior is described;
- no unnecessary dependency was introduced;
- no architectural rule was broken.

## 9. Useful documentation map

- Architecture: `docs/architecture.md`
- Data model: `docs/data-model.md`
- API: `docs/api.md`
- Backend rules: `docs/backend.md`
- Frontend rules: `docs/frontend.md`
- Barcode workflow: `docs/barcode.md`
- Kodi integration: `docs/kodi.md`
- Home Assistant integration: `docs/homeassistant.md`
- UI/UX: `docs/ui-ux.md`
- Coding style: `docs/coding-style.md`
- Testing: `docs/testing.md`
- Roadmap: `docs/roadmap.md`
- Agent prompts: `docs/prompts/`

## 10. Living document

This file and the `docs/` folder are part of the product.

When a major decision changes, update the corresponding documentation and create
or update an ADR in `docs/decisions/`.
