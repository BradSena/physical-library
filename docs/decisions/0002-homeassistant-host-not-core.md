# ADR-0002 — Home Assistant is host/integration, not core logic

## Status

Accepted

## Context

The user already uses Home Assistant extensively.

It is tempting to implement much of Avatra through HA helpers and YAML.

## Decision

Home Assistant may host Avatra and automate around it, but Avatra business logic
must stay in Avatra backend.

## Consequences

Positive:

- Avatra remains portable;
- logic is testable;
- users can run it outside HA.

Negative:

- HA integration requires explicit API/webhook design.
