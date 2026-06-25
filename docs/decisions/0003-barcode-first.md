# ADR-0003 — Barcode-first ingestion

## Status

Accepted

## Context

The collection contains hundreds of physical discs.

Manual entry would be too slow.

## Decision

The primary add workflow starts with barcode scanning.

Manual entry is fallback.

## Consequences

Positive:

- faster bulk entry;
- fewer typos;
- more pleasant UX.

Negative:

- barcode sources can be incomplete;
- unknown barcode workflow must be good.
