# Architecture

## Overview

Avatra is split into four logical layers:

1. Backend API
2. Data persistence
3. Web frontend
4. External integrations

The backend is the source of truth for Avatra-specific state.

Kodi remains the source of truth for media-center metadata.

Home Assistant is used for hosting, access, and automation orchestration, but it
must not contain core Avatra business logic.

## Backend

Technology:

- FastAPI
- SQLModel
- SQLite
- Uvicorn

Responsibilities:

- expose REST API;
- validate domain operations;
- store inventory state;
- manage physical locations;
- manage loans;
- manage barcode identification state;
- expose integration endpoints.

The backend should contain clear boundaries:

```text
app/
├── main.py
├── models/
├── schemas/
├── routes/
├── services/
├── repositories/
└── settings.py
```

If the current code is simpler, evolve gradually.

## Database

SQLite is the default database.

This is intentional:

- easy backup;
- easy Home Assistant add-on deployment;
- simple local development;
- sufficient for a home media collection.

Do not introduce PostgreSQL/MySQL as a requirement.

Future support for another DB may exist, but SQLite must remain first-class.

## Frontend

The frontend is a practical tool, not a complex SPA.

It should be:

- mobile friendly;
- fast;
- readable;
- usable on a phone while standing near shelves;
- usable through Home Assistant ingress later.

Avoid heavy frameworks unless explicitly requested.

## Kodi add-on

Kodi integration should make physical items appear naturally in Kodi workflows.

Expected behavior:

- browsing in Kodi should expose physical titles;
- launching a physical item should prompt the user to insert the disc;
- later, Avatra can trigger automation to open the correct tray and switch AVR input.

Kodi must not become the inventory database.

## Home Assistant add-on

Home Assistant integration is for:

- easy hosting;
- remote access;
- automation triggers;
- dashboards;
- notifications.

Home Assistant must not become the main storage model.

## Integration philosophy

Avatra should expose clean APIs and webhooks so other systems can integrate.

Do not hardcode the user's exact devices into core code.

Device-specific logic should live in configuration or integration adapters.

## Data flow examples

### Add a disc

1. User scans barcode.
2. Backend receives barcode.
3. Backend searches identification sources.
4. Backend proposes candidate edition.
5. User confirms or edits minimal fields.
6. Backend stores physical edition and location.

### Loan a disc

1. User selects/scans item.
2. User chooses borrower.
3. Backend creates loan record.
4. Item status changes to `on_loan`.
5. Original location is preserved.

### Return a disc

1. User scans or selects item.
2. Backend closes active loan.
3. Item status returns to `in_stock`.
4. User is reminded of original location.

### Launch a physical movie

1. User selects title in Kodi or Avatra.
2. Avatra checks availability.
3. Avatra asks user to insert disc.
4. Future automation can open tray and switch inputs.

## Non-goals

Avatra is not:

- a Plex replacement;
- a Kodi metadata scraper;
- a cloud catalog service;
- a social network;
- a commercial rental system;
- a DRM/copying tool.
