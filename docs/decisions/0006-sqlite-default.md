# ADR-0006 — SQLite as default database

## Status

Accepted

## Context

Avatra is a home/self-hosted application with modest data volume.

## Decision

SQLite is the default database.

## Consequences

Positive:

- simple deployment;
- easy backup;
- HA add-on friendly;
- no external database dependency.

Negative:

- future multi-user concurrency may require care.
