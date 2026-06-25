# API Design

The API should be simple, predictable and stable.

## Base style

Use REST-style routes.

Suggested prefix:

```text
/api
```

Use plural nouns:

```text
/api/media
/api/editions
/api/copies
/api/locations
/api/loans
/api/barcodes
/api/kodi
/api/settings
```

## Response style

Prefer explicit JSON.

Example:

```json
{
  "id": 1,
  "title": "Example",
  "created_at": "2026-06-25T10:00:00Z"
}
```

Errors should be readable:

```json
{
  "error": "barcode_not_found",
  "message": "No confident match was found for this barcode.",
  "details": {
    "barcode": "8717418373511"
  }
}
```

## Important endpoints

### Health

```text
GET /api/health
```

Returns server status.

### Media

```text
GET /api/media
POST /api/media
GET /api/media/{id}
PATCH /api/media/{id}
DELETE /api/media/{id}
```

Deletion should be careful. Prefer soft deletion once history exists.

### Barcode identification

```text
POST /api/barcodes/lookup
```

Input:

```json
{
  "barcode": "8717418373511"
}
```

Output:

```json
{
  "barcode": "8717418373511",
  "status": "matched",
  "candidates": []
}
```

Possible statuses:

- `matched`
- `multiple_candidates`
- `not_found`
- `manual_required`

### Locations

```text
GET /api/locations
POST /api/locations
PATCH /api/locations/{id}
DELETE /api/locations/{id}
```

Locations must support flexible hierarchy.

### Loans

```text
POST /api/loans
GET /api/loans
GET /api/loans/active
POST /api/loans/{id}/return
```

A loan creation must update copy status to `on_loan`.

Returning a loan must close the active loan and restore availability.

### Kodi mapping

```text
GET /api/kodi/status
POST /api/kodi/map
GET /api/kodi/mappings
```

Kodi mapping should not duplicate the Kodi library.

### Settings

```text
GET /api/settings
PATCH /api/settings
```

## API compatibility

Breaking changes require documentation.

If changing request/response shape:

1. update this file;
2. update frontend;
3. update tests;
4. mention migration impact.

## Validation

Backend must validate:

- unknown barcode;
- duplicate barcode;
- invalid status transitions;
- loaning an already loaned item;
- returning an already returned loan;
- deleting a location that still contains items.

## Future API ideas

- `/api/search`
- `/api/import/kodi`
- `/api/export`
- `/api/automation/events`
- `/api/stats`
