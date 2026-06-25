# Testing Guide

## Philosophy

Tests should protect domain rules.

The highest-value tests are around inventory state transitions.

## Priorities

Test these first:

- create media item;
- create physical edition;
- create physical copy;
- duplicate barcode handling;
- unknown barcode handling;
- loan item;
- prevent double loan;
- return item;
- preserve original location;
- mark missing;
- map to Kodi item.

## Backend tests

Use pytest if present.

Suggested test groups:

```text
tests/
├── test_barcode.py
├── test_loans.py
├── test_locations.py
├── test_media.py
├── test_kodi_mapping.py
└── test_api.py
```

## API tests

API tests should verify:

- status codes;
- response schemas;
- error messages;
- domain rule enforcement.

## Frontend tests

MVP may not need heavy frontend tests.

Manual checklist is acceptable early on.

## Manual test checklist

Before considering MVP feature done:

- start backend;
- open frontend;
- add known barcode;
- add unknown barcode manually;
- create location;
- assign item to location;
- loan item;
- return item;
- verify original location still visible;
- search collection;
- restart backend and verify persistence.

## Do not fake success

AI agents must not claim tests passed unless they actually ran.
