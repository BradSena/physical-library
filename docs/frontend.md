# Frontend Guide

## Goal

The frontend is a practical interface for managing a physical collection.

It must be usable:

- on desktop;
- on phone;
- while standing near shelves;
- through a Home Assistant panel in the future.

## Philosophy

Prefer simple HTML/CSS/JavaScript.

Avoid a heavy SPA unless the project clearly needs it.

## Core screens

MVP screens:

1. Dashboard
2. Collection list
3. Add by barcode
4. Media detail
5. Locations
6. Active loans
7. Settings

## Add by barcode screen

This is the most important UX.

Ideal flow:

1. cursor already in barcode field;
2. scan barcode;
3. automatic lookup starts;
4. if confident match, show confirmation;
5. if uncertain, show top candidates;
6. if no result, show minimal manual form.

The user should not need to click many times.

## Collection list

Should support:

- search;
- filter by status;
- filter by media type;
- filter by location;
- quick availability display.

## Media detail

Should show:

- title;
- edition;
- barcode;
- media type;
- status;
- original location;
- current location;
- active loan if any;
- Kodi mapping if any;
- history.

## Mobile-first details

Large tap targets.

Readable text.

No tiny controls.

Barcode workflow should be one-handed.

## Error messages

Messages should be clear and actionable.

Bad:

```text
500 Internal Server Error
```

Better:

```text
No reliable match was found for this barcode. You can search manually or create the edition yourself.
```

## Frontend responsibilities

Allowed:

- display data;
- call API;
- perform lightweight UI validation;
- manage local UI state.

Not allowed:

- deciding complex status transitions;
- creating hidden business rules;
- duplicating backend loan logic;
- hardcoding domain behavior that belongs to the backend.

## Future ideas

- PWA/mobile scanner;
- camera barcode scanning;
- Home Assistant panel;
- fast shelf mode;
- bulk import/review mode.
