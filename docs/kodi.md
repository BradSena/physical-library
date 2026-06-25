# Kodi Integration

## Principle

Kodi remains the user's media browsing and playback environment.

Avatra should integrate with Kodi, not replace it.

## Source of truth

Kodi owns:

- posters;
- fan art;
- synopsis;
- actors;
- genres;
- rich collection metadata;
- watched state if the user chooses.

Avatra owns:

- physical ownership;
- disc format;
- barcode;
- location;
- loan status;
- availability;
- physical edition notes.

## Desired user experience

The user should be able to browse the library naturally.

When selecting a physical disc item:

1. Kodi shows the title.
2. User selects it.
3. Avatra/Kodi add-on displays a message:
   "Insert the disc: [title]"
4. Future automation opens tray and switches AVR/projector input.

## Kodi add-on role

The add-on should:

- expose Avatra physical items;
- call Avatra backend API;
- display availability;
- trigger launch workflow;
- avoid storing inventory as its own database.

## Mapping

Kodi items may be mapped to Avatra `MediaItem`.

Mapping should use:

- title;
- year;
- optional Kodi item ID;
- manual confirmation where needed.

Do not assume title matching is always enough.

## Ripped media

Important project constraint:

The user also has Blu-ray rips on NAS that may not exist physically.

Avatra must be able to represent:

- physical disc only;
- rip only;
- both physical disc and rip;
- missing physical disc but available rip.

Do not assume every Kodi item has a physical disc.

Do not assume every physical disc has a rip.

## Launch behavior

Physical item launch is not normal video playback.

It is a workflow trigger.

Future actions may include:

- ask user to insert disc;
- open Blu-ray player tray;
- switch AVR input;
- dim lights;
- set projector mode;
- start cinema mode.

## Non-goals

The Kodi integration must not:

- scrape the whole internet;
- become the backend;
- duplicate all Kodi metadata;
- require replacing the user's existing Kodi library.
