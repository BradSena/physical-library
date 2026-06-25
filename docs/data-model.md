# Data Model

This document describes the intended domain model.

Names may differ in current implementation, but future code should converge
toward these concepts.

## Core concepts

Avatra distinguishes:

- a movie/work/title;
- a physical edition;
- a physical copy;
- a location;
- a current state;
- a history of movements/events.

This is important because the same movie can exist in multiple forms:

- DVD
- Blu-ray
- UHD
- steelbook
- collector box
- NAS rip
- special edition

## MediaItem

Represents the abstract title or work.

Example:

```text
Pirates of the Caribbean: The Curse of the Black Pearl
```

Fields:

- id
- title
- original_title
- year
- media_category
- notes
- created_at
- updated_at

MediaItem is not necessarily physical.

It may correspond to a Kodi movie.

## PhysicalEdition

Represents a specific edition/package.

Examples:

- French Blu-ray edition
- UHD steelbook
- DVD collector box
- boxset entry

Fields:

- id
- media_item_id
- media_type
- edition_label
- region
- publisher
- release_year
- barcode
- packaging
- notes
- created_at
- updated_at

## PhysicalCopy

Represents one actual object owned by the user.

For many home collections, one edition equals one copy, but the distinction is
useful for future-proofing.

Fields:

- id
- physical_edition_id
- original_location_id
- current_location_id
- status
- acquisition_date
- condition
- notes
- created_at
- updated_at

## Status

Allowed statuses should be explicit.

Initial set:

- `in_stock`
- `on_loan`
- `on_display`
- `missing`
- `digitized_only`
- `archived`

Rules:

- `on_loan` requires an active loan.
- `in_stock` should normally have a current location.
- `missing` should preserve the last known location.
- A loan must never erase original location.

## Location

Represents a physical or logical place.

Examples:

- Shelf A / Level 1
- Column B
- Display shelf
- Loaned to Julien
- NAS
- Temporary pile

Fields:

- id
- name
- parent_id
- type
- sort_order
- capacity_hint
- notes
- created_at
- updated_at

Important rule:

Do not force fixed slot numbering.

The user may choose coarse locations.

## Loan

Represents a lending event.

Fields:

- id
- physical_copy_id
- borrower_id
- loaned_at
- expected_return_at
- returned_at
- notes
- created_at
- updated_at

Rules:

- one physical copy can have at most one active loan;
- closing a loan should restore the item to stock or ask for confirmation;
- original location remains preserved.

## Holder / Borrower

Represents a person or entity that can hold an item.

Fields:

- id
- display_name
- contact_info
- notes
- created_at
- updated_at

Keep personal data minimal.

## Barcode

Barcode may be stored directly on PhysicalEdition, but a separate table is useful
if multiple codes map to the same edition.

Fields:

- id
- code
- format
- physical_edition_id
- source
- confidence
- created_at

## KodiMapping

Links Avatra entities to Kodi library entries.

Fields:

- id
- media_item_id
- kodi_item_id
- kodi_library_type
- kodi_title
- kodi_year
- confidence
- created_at
- updated_at

Rules:

- Kodi metadata remains in Kodi.
- Store only enough data to map reliably.

## InventoryEvent

Append-only history of important actions.

Event types:

- created
- identified
- location_changed
- loaned
- returned
- marked_missing
- marked_found
- displayed
- removed_from_display
- mapped_to_kodi
- notes_updated

Fields:

- id
- entity_type
- entity_id
- event_type
- payload_json
- created_at

History is important because physical collections drift over time.

## Settings

Stores user configuration.

Examples:

- default location
- barcode source preferences
- Kodi endpoint
- Home Assistant integration settings
- UI preferences

Settings should be explicit and exportable.

## Naming conventions

Use precise names.

Avoid generic names like `Item` when `PhysicalCopy` is meant.

Avoid mixing Kodi item identity with physical copy identity.

## Migration guidance

If the current DB model is simpler:

- do not rewrite everything at once;
- introduce missing concepts gradually;
- preserve data;
- create migration notes in docs.
