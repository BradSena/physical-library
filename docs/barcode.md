# Barcode Workflow

## Principle

Barcode scanning is the default entry method.

Manual entry is a fallback.

## Why barcode first?

The user owns hundreds of discs.

Typing titles manually is unacceptable.

The system should reduce effort as much as possible.

## Basic flow

1. User scans barcode.
2. Backend receives barcode.
3. Backend searches available identification sources.
4. Backend returns candidates.
5. User confirms or selects.
6. Avatra creates the physical edition/copy.

## Candidate confidence

Results should be ranked.

Possible outcomes:

- confident single match;
- multiple plausible candidates;
- no match;
- conflicting sources.

The UI should expose uncertainty honestly.

## Sources

Potential sources may include:

- public web search;
- barcode databases;
- retailer pages;
- user-provided manual entry;
- future local cache.

Avoid mandatory paid APIs.

Avoid building a full metadata scraper.

The goal is identification, not full movie metadata replacement.

## Stored data

Store only what Avatra needs:

- title;
- year if known;
- media type;
- edition label;
- barcode;
- source/confidence;
- notes.

Kodi can later enrich display metadata.

## Failure flow

If no confident result:

1. show barcode;
2. ask for minimal fields:
   - title;
   - media type;
   - optional year;
   - optional edition label;
3. save as manual entry;
4. allow future correction.

## Duplicate barcode

If a barcode already exists:

- do not silently create a duplicate;
- show existing item;
- allow adding another copy only if intentional.

## Scanner support

USB barcode scanners usually behave like keyboards.

The UI should handle rapid input followed by Enter.

Future camera scanning can be added later.

## Test barcode

Known test barcode from previous development:

```text
8717418373511
```

Do not hardcode special behavior for it.
