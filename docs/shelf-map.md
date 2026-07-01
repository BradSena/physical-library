# Shelf Map

The Shelf Map is a future Avatra module for representing the approximate
physical geometry of a media shelf and assigning scanned discs to positions
inside that geometry.

It supports Avatra's core role: Kodi knows the movie; Avatra knows the disc.

## Core Concepts

- `Shelf`: a physical storage unit, such as a bookcase, media cabinet or wall
  shelf.
- `Column`: a vertical section of a shelf.
- `Level`: one horizontal row inside a column.
- `Slot`: the actual disc position assigned during scanning.

## Design Principle

The shelf map represents approximate physical geometry. It does not enforce
exact capacity.

Estimated capacity is only used for visual scale. The real inventory is defined
by scanned positions.

This keeps the location model flexible: users can use coarse locations, precise
slot positions or a mix of both without Avatra forcing a rigid shelf model.

## Visual Shelf Creation

Users can create a shelf visually.

They add columns one by one. For each column, users define:

- `name`
- `width_cm`
- `number_of_levels`

Avatra uses `width_cm` and media type assumptions to estimate an approximate
capacity per level. For example, Blu-ray and DVD cases may have different
estimated widths.

These estimates are not validation rules. They only help draw a proportional
visual map and give the user a sense of available space.

## Scan Sessions

A scan session can start by selecting a shelf, column and level in the visual
shelf map.

During that scan session:

1. The user selects a target shelf column level.
2. The user scans discs in physical order.
3. Each scanned disc receives the next position in that selected level.
4. Avatra stores the resulting physical location metadata.

Actual disc count and actual positions come from this scan flow, not from the
estimated capacity.

## Moving Discs

Later, users can move discs or groups of discs by drag and drop in the shelf
map.

Drag and drop updates physical location metadata in the database. Moving a disc
does not change the movie identity or Kodi metadata; it only changes Avatra's
physical inventory state.

Group moves should support common real-world actions such as shifting a run of
discs to make room, moving a series to another level or relocating a whole shelf
section.

## Future Integrations

The Shelf Map can later be used to:

- show a highlighted disc location in Kodi;
- drive addressable LEDs;
- generate a visual map image for Kodi.

These integrations should consume Avatra's physical location data rather than
becoming the source of truth themselves.

## Non-Goals

The Shelf Map should not:

- enforce exact capacity;
- block scanning because an estimated level is "full";
- require every user to manage precise slots;
- replace flexible manual location workflows.

Manual and approximate location workflows remain valid fallbacks.
