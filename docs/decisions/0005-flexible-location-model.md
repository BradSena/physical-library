# ADR-0005 — Flexible location model

## Status

Accepted

## Context

The user may organize shelves aesthetically, by series, by columns, by levels or
rough zones.

A rigid slot model would be annoying.

## Decision

Locations are flexible and hierarchical.

Exact slots are optional, not mandatory.

## Consequences

Positive:

- matches real-world behavior;
- supports coarse or precise organization.

Negative:

- less automatic capacity validation early on.
