# Backend Guide

## Stack

Backend stack:

- Python
- FastAPI
- SQLModel
- SQLite

## Responsibilities

The backend owns:

- domain rules;
- database writes;
- validation;
- API contracts;
- integration adapters;
- history events.

The frontend must not duplicate important business rules.

## Suggested structure

```text
backend/app/
├── main.py
├── database.py
├── models/
├── schemas/
├── routes/
├── services/
├── repositories/
├── integrations/
└── tests/
```

## Models

Models should represent domain concepts.

Avoid one giant model.

Prefer explicit relationships.

## Services

Services contain business logic.

Examples:

- `BarcodeService`
- `InventoryService`
- `LoanService`
- `LocationService`
- `KodiMappingService`

Routes should be thin.

## Repositories

Repositories contain persistence logic if/when the codebase grows enough.

At MVP stage, direct SQLModel usage in services may be acceptable, but avoid
spreading complex queries everywhere.

## Error handling

Use meaningful errors.

Avoid returning plain strings for structured errors.

Recommended pattern:

- domain exception in service;
- route catches/translates to HTTPException or error schema.

## Configuration

Configuration should support:

- development defaults;
- Home Assistant add-on paths;
- local SQLite path;
- Kodi endpoint;
- logging verbosity.

Do not hardcode Nicolas's local paths or devices into generic code.

## Logging

Log:

- startup;
- DB path;
- barcode lookup failures;
- integration connection failures;
- unexpected exceptions.

Do not log sensitive contact details unnecessarily.

## Database migrations

If Alembic is not yet introduced, be cautious with schema changes.

For early MVP, manual reset may be acceptable, but document it.

For beta, introduce a migration strategy.

## Performance

Expected scale:

- hundreds to a few thousand media items;
- small number of concurrent users;
- home server/NAS/HA add-on environment.

Optimize for simplicity first.

## Security

Assume local network use first.

Future remote access via Home Assistant should respect HA authentication.

Do not expose destructive endpoints without thought.

## Testing priorities

High-value backend tests:

- barcode not found;
- duplicate barcode;
- create item;
- loan item;
- return item;
- preserve original location;
- invalid status transition;
- Kodi mapping persistence.
