# Home Assistant Integration

## Principle

Home Assistant is an excellent host and automation coordinator.

It is not the core Avatra business logic engine.

## Roles

Home Assistant may provide:

- add-on hosting;
- ingress access;
- dashboards;
- automations;
- notifications;
- device control.

Avatra backend provides:

- inventory API;
- media state;
- loan state;
- barcode workflow;
- Kodi mapping;
- launch workflow events.

## Add-on goals

The Home Assistant add-on should make installation easy.

Expected:

- install Avatra as add-on;
- expose web UI through ingress;
- persist SQLite database in add-on data;
- allow backup with HA backups;
- configure port and paths.

## Automation examples

Future HA automations may react to Avatra events:

- physical movie selected;
- disc insertion requested;
- cinema mode requested;
- item loan overdue;
- item returned;
- media missing.

## Device-specific logic

Do not hardcode the user's exact devices into Avatra core.

Examples of user-specific devices that should remain configurable:

- AVR entity;
- projector;
- Blu-ray player;
- lighting scenes;
- disc tray command;
- HomePod announcements.

## Security

If exposed through HA ingress, rely on HA authentication.

Avoid building an unrelated auth system too early.

## API/webhooks

Useful future endpoints:

```text
POST /api/automation/movie-selected
POST /api/automation/disc-requested
GET /api/automation/events
```

But keep MVP simple.

## Non-goals

Home Assistant integration must not:

- store the main inventory in HA helpers;
- require YAML for normal collection management;
- make Avatra unusable outside HA.
