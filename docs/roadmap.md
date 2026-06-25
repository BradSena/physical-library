# Roadmap

## Phase 0 — Foundations

Status: mostly started.

Goals:

- repository structure;
- FastAPI backend;
- SQLite database;
- basic frontend shell;
- documentation;
- AI agent instructions.

## Phase 1 — Inventory MVP

Goals:

- create media items;
- create physical editions;
- create locations;
- assign items to locations;
- list/search collection;
- edit basic data.

Success:

The user can enter a meaningful part of the collection and find where discs are.

## Phase 2 — Barcode workflow

Goals:

- barcode lookup endpoint;
- candidate results;
- manual fallback;
- duplicate barcode handling;
- fast scan UI.

Success:

The user can add discs by scanning barcodes with minimal typing.

## Phase 3 — Loans and status

Goals:

- borrowers/holders;
- loan item;
- return item;
- active loans list;
- preserve original location;
- history events.

Success:

The user can lend discs without losing track of where they belong.

## Phase 4 — Kodi integration

Goals:

- Kodi add-on talks to backend;
- browse Avatra items;
- map Avatra items to Kodi titles;
- display physical availability;
- launch physical-disc workflow.

Success:

The user can browse physical media from Kodi and get insert-disc behavior.

## Phase 5 — Home Assistant add-on

Goals:

- package Avatra as HA add-on;
- ingress;
- persistent data path;
- configuration;
- backup-friendly layout.

Success:

The user can install and access Avatra from Home Assistant.

## Phase 6 — Home cinema automation

Goals:

- movie selected event;
- disc requested event;
- integration hooks;
- configurable automation targets;
- optional cinema mode.

Success:

Selecting a film can prepare the room with minimal interaction.

## Phase 7 — Polish

Goals:

- improved UI;
- import/export;
- backup;
- stats;
- better search;
- mobile camera scanner;
- documentation cleanup.

## Deferred ideas

- commercial rental workflows;
- social sharing;
- complex user accounts;
- full metadata scraping;
- mandatory cloud sync;
- replacing Kodi.
