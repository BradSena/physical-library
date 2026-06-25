# ADR-0001 — Kodi remains the metadata source of truth

## Status

Accepted

## Context

Kodi already provides rich media metadata and browsing.

Avatra's unique value is physical inventory, not replacing Kodi.

## Decision

Avatra will not implement a full movie metadata system.

Kodi remains responsible for:

- posters;
- synopsis;
- fan art;
- actors;
- collections;
- playback library.

Avatra stores only what it needs for physical inventory and mapping.

## Consequences

Positive:

- less complexity;
- respects user's existing setup;
- faster MVP.

Negative:

- Avatra depends on Kodi for rich display metadata;
- mapping may require manual confirmation.
