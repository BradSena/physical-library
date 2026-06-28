import json
import sqlite3
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.lookup.search import lookup


DB_PATH = Path("avatra.db")

TECHNICAL_METADATA_COLUMNS = {
    "resolution": "TEXT",
    "video_codec": "TEXT",
    "hdr": "TEXT",
    "aspect_ratio": "TEXT",
    "original_aspect_ratio": "TEXT",
    "audio_tracks": "TEXT",
    "spoken_languages": "TEXT",
    "subtitles": "TEXT",
    "region": "TEXT",
    "runtime": "INTEGER",
    "discs": "INTEGER",
}

STOCK_COLUMNS = {
    "current_location": "TEXT",
    "holder_name": "TEXT",
    "loan_date": "TEXT",
    "notes": "TEXT",
}

SHELF_LOCATION_COLUMNS = {
    "shelf_level_id": "INTEGER",
    "shelf_position": "INTEGER",
}

LIST_METADATA_FIELDS = {
    "hdr",
    "audio_tracks",
    "spoken_languages",
    "subtitles",
}

EDITABLE_FIELDS = {
    "title",
    "year",
    "media_type",
    "edition_label",
    "original_location",
    "resolution",
    "video_codec",
    "hdr",
    "aspect_ratio",
    "original_aspect_ratio",
    "audio_tracks",
    "spoken_languages",
    "subtitles",
    "region",
    "runtime",
    "discs",
    "current_state",
    "current_location",
    "holder_name",
    "loan_date",
    "notes",
}


class PhysicalItem(BaseModel):
    id: int | None = None
    barcode: str | None = None
    title: str
    year: int | None = None
    media_type: str = "bluray"
    edition_label: str | None = None
    original_location: str | None = None
    current_location: str | None = None
    current_state: str = "in_stock"
    temporary_holder: str | None = None
    holder_name: str | None = None
    loan_date: str | None = None
    notes: str | None = None
    shelf_level_id: int | None = None
    shelf_position: int | None = None

    resolution: str | None = None
    video_codec: str | None = None
    hdr: list[str] = []
    aspect_ratio: str | None = None
    original_aspect_ratio: str | None = None
    audio_tracks: list[str] = []
    spoken_languages: list[str] = []
    subtitles: list[str] = []
    region: str | None = None
    runtime: int | None = None
    discs: int | None = None


class PhysicalItemUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    media_type: str | None = None
    edition_label: str | None = None
    original_location: str | None = None
    current_location: str | None = None
    current_state: str | None = None
    holder_name: str | None = None
    loan_date: str | None = None
    notes: str | None = None

    resolution: str | None = None
    video_codec: str | None = None
    hdr: list[str] | None = None
    aspect_ratio: str | None = None
    original_aspect_ratio: str | None = None
    audio_tracks: list[str] | None = None
    spoken_languages: list[str] | None = None
    subtitles: list[str] | None = None
    region: str | None = None
    runtime: int | None = None
    discs: int | None = None


class LoanRequest(BaseModel):
    holder_name: str


class DisplayRequest(BaseModel):
    current_location: str | None = None


class ShelfLevel(BaseModel):
    id: int | None = None
    column_id: int | None = None
    level_index: int
    estimated_capacity: int | None = None


class ShelfColumn(BaseModel):
    id: int | None = None
    shelf_id: int | None = None
    name: str
    width_cm: int | None = None
    sort_order: int = 0
    levels: list[ShelfLevel] = []


class Shelf(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    columns: list[ShelfColumn] = []


class ShelfCreate(BaseModel):
    name: str
    description: str | None = None


class ShelfUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ShelfColumnCreate(BaseModel):
    name: str
    width_cm: int | None = None
    level_count: int


class ShelfColumnUpdate(BaseModel):
    name: str | None = None
    width_cm: int | None = None
    sort_order: int | None = None


class ShelfLevelUpdate(BaseModel):
    estimated_capacity: int | None = None


class ItemLocationRequest(BaseModel):
    shelf_level_id: int
    shelf_position: int


app = FastAPI(title="Avatra", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def encode_list_metadata(value: list[str] | None) -> str:
    return json.dumps(value or [])


def decode_list_metadata(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        return []
    return decoded if isinstance(decoded, list) else []


def item_from_row(row: sqlite3.Row) -> dict:
    item = dict(row)
    for field in LIST_METADATA_FIELDS:
        item[field] = decode_list_metadata(item.get(field))
    return item


def estimate_level_capacity(width_cm: int | None) -> int | None:
    if width_cm is None:
        return None
    return int(width_cm / 1.4)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS physical_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT,
                title TEXT NOT NULL,
                year INTEGER,
                media_type TEXT NOT NULL DEFAULT 'bluray',
                edition_label TEXT,
                original_location TEXT,
                current_location TEXT,
                current_state TEXT NOT NULL DEFAULT 'in_stock',
                temporary_holder TEXT,
                holder_name TEXT,
                loan_date TEXT,
                notes TEXT,
                resolution TEXT,
                video_codec TEXT,
                hdr TEXT,
                aspect_ratio TEXT,
                original_aspect_ratio TEXT,
                audio_tracks TEXT,
                spoken_languages TEXT,
                subtitles TEXT,
                region TEXT,
                runtime INTEGER,
                discs INTEGER,
                shelf_level_id INTEGER,
                shelf_position INTEGER
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shelves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shelf_columns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shelf_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                width_cm INTEGER,
                sort_order INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (shelf_id) REFERENCES shelves(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shelf_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                column_id INTEGER NOT NULL,
                level_index INTEGER NOT NULL,
                estimated_capacity INTEGER,
                FOREIGN KEY (column_id) REFERENCES shelf_columns(id)
            )
            """
        )
        existing_columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(physical_items)").fetchall()
        }

        for column, column_type in TECHNICAL_METADATA_COLUMNS.items():
            if column not in existing_columns:
                conn.execute(
                    f"ALTER TABLE physical_items ADD COLUMN {column} {column_type}"
                )

        for column, column_type in STOCK_COLUMNS.items():
            if column not in existing_columns:
                conn.execute(
                    f"ALTER TABLE physical_items ADD COLUMN {column} {column_type}"
                )

        for column, column_type in SHELF_LOCATION_COLUMNS.items():
            if column not in existing_columns:
                conn.execute(
                    f"ALTER TABLE physical_items ADD COLUMN {column} {column_type}"
                )

        conn.commit()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def web_app():
    return FileResponse("app/static/index.html")


@app.get("/api")
def api_root():
    return {
        "name": "Avatra",
        "tagline": "Digital avatars for your physical media.",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/lookup/{barcode}")
async def barcode_lookup(barcode: str):
    return await lookup(barcode)


def shelf_from_row(conn: sqlite3.Connection, row: sqlite3.Row) -> dict:
    shelf = dict(row)
    column_rows = conn.execute(
        """
        SELECT *
        FROM shelf_columns
        WHERE shelf_id = ?
        ORDER BY sort_order ASC, id ASC
        """,
        (shelf["id"],),
    ).fetchall()

    columns = []
    for column_row in column_rows:
        column = dict(column_row)
        level_rows = conn.execute(
            """
            SELECT *
            FROM shelf_levels
            WHERE column_id = ?
            ORDER BY level_index ASC
            """,
            (column["id"],),
        ).fetchall()
        column["levels"] = [dict(level_row) for level_row in level_rows]
        columns.append(column)

    shelf["columns"] = columns
    return shelf


def get_shelf_or_404(conn: sqlite3.Connection, shelf_id: int) -> dict:
    row = conn.execute(
        "SELECT * FROM shelves WHERE id = ?",
        (shelf_id,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Shelf not found.")
    return shelf_from_row(conn, row)


def get_column_or_404(conn: sqlite3.Connection, column_id: int) -> dict:
    row = conn.execute(
        "SELECT * FROM shelf_columns WHERE id = ?",
        (column_id,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Shelf column not found.")
    return dict(row)


def get_level_location(conn: sqlite3.Connection, level_id: int) -> dict:
    row = conn.execute(
        """
        SELECT
            shelf_levels.id AS level_id,
            shelf_levels.level_index,
            shelf_columns.name AS column_name,
            shelves.name AS shelf_name
        FROM shelf_levels
        JOIN shelf_columns ON shelf_columns.id = shelf_levels.column_id
        JOIN shelves ON shelves.id = shelf_columns.shelf_id
        WHERE shelf_levels.id = ?
        """,
        (level_id,),
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Shelf level not found.")
    return dict(row)


@app.get("/shelves")
def list_shelves():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM shelves ORDER BY id ASC").fetchall()
        return [shelf_from_row(conn, row) for row in rows]


@app.post("/shelves")
def create_shelf(shelf: ShelfCreate):
    name = shelf.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Shelf name is required.")

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO shelves (name, description) VALUES (?, ?)",
            (name, shelf.description),
        )
        conn.commit()
        return get_shelf_or_404(conn, cursor.lastrowid)


@app.patch("/shelves/{shelf_id}")
def update_shelf(shelf_id: int, shelf_update: ShelfUpdate):
    updates = shelf_update.model_dump(exclude_unset=True)
    if not updates:
        with get_connection() as conn:
            return get_shelf_or_404(conn, shelf_id)

    if "name" in updates:
        updates["name"] = updates["name"].strip() if updates["name"] else ""
        if not updates["name"]:
            raise HTTPException(status_code=400, detail="Shelf name is required.")

    assignments = ", ".join(f"{field} = ?" for field in updates)

    with get_connection() as conn:
        cursor = conn.execute(
            f"UPDATE shelves SET {assignments} WHERE id = ?",
            (*updates.values(), shelf_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Shelf not found.")
        conn.commit()
        return get_shelf_or_404(conn, shelf_id)


@app.delete("/shelves/{shelf_id}")
def delete_shelf(shelf_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM shelves WHERE id = ?",
            (shelf_id,),
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Shelf not found.")

        conn.execute(
            """
            UPDATE physical_items
            SET shelf_level_id = NULL, shelf_position = NULL
            WHERE shelf_level_id IN (
                SELECT shelf_levels.id
                FROM shelf_levels
                JOIN shelf_columns ON shelf_columns.id = shelf_levels.column_id
                WHERE shelf_columns.shelf_id = ?
            )
            """,
            (shelf_id,),
        )
        conn.execute(
            """
            DELETE FROM shelf_levels
            WHERE column_id IN (
                SELECT id FROM shelf_columns WHERE shelf_id = ?
            )
            """,
            (shelf_id,),
        )
        conn.execute("DELETE FROM shelf_columns WHERE shelf_id = ?", (shelf_id,))
        conn.execute("DELETE FROM shelves WHERE id = ?", (shelf_id,))
        conn.commit()
    return {"deleted": True}


@app.post("/shelves/{shelf_id}/columns")
def create_shelf_column(shelf_id: int, column: ShelfColumnCreate):
    name = column.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Column name is required.")
    if column.level_count < 1:
        raise HTTPException(status_code=400, detail="Level count must be at least 1.")

    estimated_capacity = estimate_level_capacity(column.width_cm)

    with get_connection() as conn:
        get_shelf_or_404(conn, shelf_id)
        cursor = conn.execute(
            """
            INSERT INTO shelf_columns (shelf_id, name, width_cm)
            VALUES (?, ?, ?)
            """,
            (shelf_id, name, column.width_cm),
        )
        column_id = cursor.lastrowid

        for level_index in range(1, column.level_count + 1):
            conn.execute(
                """
                INSERT INTO shelf_levels (
                    column_id, level_index, estimated_capacity
                )
                VALUES (?, ?, ?)
                """,
                (column_id, level_index, estimated_capacity),
            )

        conn.commit()
        created = get_column_or_404(conn, column_id)
        created["levels"] = [
            dict(row)
            for row in conn.execute(
                """
                SELECT *
                FROM shelf_levels
                WHERE column_id = ?
                ORDER BY level_index ASC
                """,
                (column_id,),
            ).fetchall()
        ]
        return created


@app.patch("/shelf-columns/{column_id}")
def update_shelf_column(column_id: int, column_update: ShelfColumnUpdate):
    updates = column_update.model_dump(exclude_unset=True)
    if not updates:
        with get_connection() as conn:
            column = get_column_or_404(conn, column_id)
            column["levels"] = [
                dict(row)
                for row in conn.execute(
                    """
                    SELECT *
                    FROM shelf_levels
                    WHERE column_id = ?
                    ORDER BY level_index ASC
                    """,
                    (column_id,),
                ).fetchall()
            ]
            return column

    if "name" in updates:
        updates["name"] = updates["name"].strip() if updates["name"] else ""
        if not updates["name"]:
            raise HTTPException(status_code=400, detail="Column name is required.")

    assignments = ", ".join(f"{field} = ?" for field in updates)

    with get_connection() as conn:
        cursor = conn.execute(
            f"UPDATE shelf_columns SET {assignments} WHERE id = ?",
            (*updates.values(), column_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Shelf column not found.")
        conn.commit()

        column = get_column_or_404(conn, column_id)
        column["levels"] = [
            dict(row)
            for row in conn.execute(
                """
                SELECT *
                FROM shelf_levels
                WHERE column_id = ?
                ORDER BY level_index ASC
                """,
                (column_id,),
            ).fetchall()
        ]
        return column


@app.delete("/shelf-columns/{column_id}")
def delete_shelf_column(column_id: int):
    with get_connection() as conn:
        get_column_or_404(conn, column_id)
        conn.execute(
            """
            UPDATE physical_items
            SET shelf_level_id = NULL, shelf_position = NULL
            WHERE shelf_level_id IN (
                SELECT id FROM shelf_levels WHERE column_id = ?
            )
            """,
            (column_id,),
        )
        conn.execute("DELETE FROM shelf_levels WHERE column_id = ?", (column_id,))
        conn.execute("DELETE FROM shelf_columns WHERE id = ?", (column_id,))
        conn.commit()
    return {"deleted": True}


@app.patch("/shelf-levels/{level_id}")
def update_shelf_level(level_id: int, level_update: ShelfLevelUpdate):
    updates = level_update.model_dump(exclude_unset=True)
    with get_connection() as conn:
        if not updates:
            row = conn.execute(
                "SELECT * FROM shelf_levels WHERE id = ?",
                (level_id,),
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Shelf level not found.")
            return dict(row)

        cursor = conn.execute(
            """
            UPDATE shelf_levels
            SET estimated_capacity = ?
            WHERE id = ?
            """,
            (updates.get("estimated_capacity"), level_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Shelf level not found.")
        conn.commit()
        row = conn.execute(
            "SELECT * FROM shelf_levels WHERE id = ?",
            (level_id,),
        ).fetchone()
        return dict(row)


@app.get("/items")
def list_items():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM physical_items ORDER BY id DESC").fetchall()
        return [item_from_row(row) for row in rows]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM physical_items WHERE id = ?",
            (item_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found.")

    return item_from_row(row)


@app.post("/items")
def create_item(item: PhysicalItem):
    if item.current_location is None:
        item.current_location = item.original_location

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO physical_items (
                barcode, title, year, media_type, edition_label,
                original_location, current_location, current_state,
                temporary_holder, holder_name, loan_date, notes,
                resolution, video_codec, hdr, aspect_ratio,
                original_aspect_ratio, audio_tracks, spoken_languages,
                subtitles, region, runtime, discs,
                shelf_level_id, shelf_position
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.barcode,
                item.title,
                item.year,
                item.media_type,
                item.edition_label,
                item.original_location,
                item.current_location,
                item.current_state,
                item.temporary_holder,
                item.holder_name,
                item.loan_date,
                item.notes,
                item.resolution,
                item.video_codec,
                encode_list_metadata(item.hdr),
                item.aspect_ratio,
                item.original_aspect_ratio,
                encode_list_metadata(item.audio_tracks),
                encode_list_metadata(item.spoken_languages),
                encode_list_metadata(item.subtitles),
                item.region,
                item.runtime,
                item.discs,
                item.shelf_level_id,
                item.shelf_position,
            ),
        )
        conn.commit()
        item.id = cursor.lastrowid
    return item


def update_item_fields(item_id: int, updates: dict):
    if not updates:
        return get_item(item_id)

    values = [
        encode_list_metadata(value) if field in LIST_METADATA_FIELDS else value
        for field, value in updates.items()
    ]
    assignments = ", ".join(f"{field} = ?" for field in updates)

    with get_connection() as conn:
        cursor = conn.execute(
            f"UPDATE physical_items SET {assignments} WHERE id = ?",
            (*values, item_id),
        )
        conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found.")

    return get_item(item_id)


@app.patch("/items/{item_id}")
def update_item(item_id: int, item_update: PhysicalItemUpdate):
    updates = item_update.model_dump(exclude_unset=True)
    updates = {
        key: value
        for key, value in updates.items()
        if key in EDITABLE_FIELDS
    }

    if not updates:
        return get_item(item_id)

    if "title" in updates and not updates["title"]:
        raise HTTPException(status_code=400, detail="Title is required.")

    return update_item_fields(item_id, updates)


@app.post("/items/{item_id}/stock/in-stock")
def mark_item_in_stock(item_id: int):
    item = get_item(item_id)
    return update_item_fields(
        item_id,
        {
            "current_state": "in_stock",
            "current_location": item.get("original_location"),
            "holder_name": None,
            "loan_date": None,
        },
    )


@app.post("/items/{item_id}/stock/on-loan")
def mark_item_on_loan(item_id: int, loan: LoanRequest):
    holder_name = loan.holder_name.strip()
    if not holder_name:
        raise HTTPException(status_code=400, detail="Holder name is required.")

    return update_item_fields(
        item_id,
        {
            "current_state": "on_loan",
            "current_location": None,
            "holder_name": holder_name,
            "loan_date": date.today().isoformat(),
        },
    )


@app.post("/items/{item_id}/stock/on-display")
def mark_item_on_display(item_id: int, display: DisplayRequest | None = None):
    item = get_item(item_id)
    display_location = display.current_location if display else None
    current_location = display_location or item.get("original_location")

    return update_item_fields(
        item_id,
        {
            "current_state": "on_display",
            "current_location": current_location,
            "holder_name": None,
            "loan_date": None,
        },
    )


@app.post("/items/{item_id}/stock/missing")
def mark_item_missing(item_id: int):
    return update_item_fields(
        item_id,
        {
            "current_state": "missing",
            "current_location": None,
            "holder_name": None,
            "loan_date": None,
        },
    )


@app.post("/items/{item_id}/location")
def assign_item_location(item_id: int, location: ItemLocationRequest):
    if location.shelf_position < 1:
        raise HTTPException(
            status_code=400,
            detail="Shelf position must be at least 1.",
        )

    with get_connection() as conn:
        level = get_level_location(conn, location.shelf_level_id)
        item = conn.execute(
            "SELECT id FROM physical_items WHERE id = ?",
            (item_id,),
        ).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found.")

        location_label = (
            f"{level['shelf_name']} / {level['column_name']} / "
            f"Level {level['level_index']} / Position {location.shelf_position}"
        )

        conn.execute(
            """
            UPDATE physical_items
            SET
                shelf_level_id = ?,
                shelf_position = ?,
                original_location = ?,
                current_location = ?
            WHERE id = ?
            """,
            (
                location.shelf_level_id,
                location.shelf_position,
                location_label,
                location_label,
                item_id,
            ),
        )
        conn.commit()

    return get_item(item_id)


@app.post("/scan/{barcode}")
async def scan_barcode(barcode: str):
    lookup_result = await lookup(barcode)

    if not lookup_result.get("found"):
        return {
            "created": False,
            "manual_required": True,
            "message": "Barcode not recognized.",
        }

    result = lookup_result["result"]

    item = PhysicalItem(
        barcode=barcode,
        title=result["title"],
        year=result.get("year"),
        media_type=result.get("media_type", "bluray"),
        edition_label=result.get("edition_label"),
        current_state="in_stock",
        resolution=result.get("resolution"),
        video_codec=result.get("video_codec"),
        hdr=result.get("hdr") or [],
        aspect_ratio=result.get("aspect_ratio"),
        original_aspect_ratio=result.get("original_aspect_ratio"),
        audio_tracks=result.get("audio_tracks") or [],
        spoken_languages=result.get("spoken_languages") or [],
        subtitles=result.get("subtitles") or [],
        region=result.get("region"),
        runtime=result.get("runtime"),
        discs=result.get("discs"),
    )

    return {
        "created": True,
        "item": create_item(item),
        "lookup": lookup_result,
    }
