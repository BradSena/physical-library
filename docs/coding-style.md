# Coding Style

## General

Prefer clarity over cleverness.

The project should remain understandable to a non-professional developer with AI
assistance.

## Python

Use:

- type hints;
- explicit names;
- small functions;
- Pydantic/SQLModel schemas;
- clear service boundaries.

Avoid:

- magical metaprogramming;
- hidden global state;
- unnecessary async complexity;
- broad `except Exception` without logging/context.

## FastAPI

Routes should be thin.

Business logic should live in services.

Example route responsibility:

- parse request;
- call service;
- return response.

Example service responsibility:

- validate domain rules;
- mutate database;
- create history events;
- return result.

## SQLModel

Keep models explicit.

Prefer relationships only when useful.

Avoid making the database schema more complex than the domain requires.

## JavaScript

Use modern vanilla JS unless a frontend framework is explicitly introduced.

Avoid business-critical logic in JS.

## CSS

Keep CSS simple.

Prefer layout clarity over visual complexity.

## Naming

Use domain words:

- `PhysicalCopy`
- `PhysicalEdition`
- `Loan`
- `Location`
- `BarcodeLookup`

Avoid vague names:

- `Thing`
- `ItemData`
- `Manager`
- `Stuff`

## Comments

Comments should explain why, not what.

## Dependencies

Before adding a dependency, ask:

- Is it necessary?
- Is it maintained?
- Does it work self-hosted?
- Does it add cloud lock-in?
- Is the feature worth the complexity?

## Formatting

Use standard Python formatting tools if present in repo.

Do not introduce a new formatter without documenting it.
