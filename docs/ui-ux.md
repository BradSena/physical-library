# UI / UX Guide

## User profile

The main user is a home-cinema enthusiast, not a software developer.

The interface must be practical, forgiving and fast.

## UX principles

- Reduce typing.
- Prefer scanning.
- Prefer sensible defaults.
- Make uncertainty visible.
- Make recovery easy.
- Do not require perfect cataloging before the app is useful.

## Key scenarios

### Adding discs in bulk

The user may stand near shelves with many discs.

The app should support fast repeated scanning.

Ideal:

1. select default location once;
2. scan disc;
3. confirm result;
4. auto-increment/order if relevant;
5. ready for next scan.

## Location precision

Do not force exact slots.

Some users want:

- shelf;
- level;
- column;
- box;
- display area.

The UI must allow coarse locations.

## Loans

Loan workflow should be simple:

1. scan/select item;
2. choose borrower;
3. save.

Return workflow:

1. scan/select item;
2. mark returned;
3. show original location.

## Empty states

Good empty states matter.

Examples:

- "No media yet. Start by scanning a barcode."
- "No active loans."
- "No location configured. Create your first shelf."

## Error handling

Errors should include next action.

Example:

```text
This barcode is already linked to another item.
Open existing item or add a second copy?
```

## Accessibility

Use readable contrast.

Avoid tiny buttons.

Support keyboard use.

## Future UX ideas

- mobile camera scanner;
- shelf mode;
- batch import;
- display/expo mode;
- evening movie shortlist;
- "choose a movie for tonight" mode.
