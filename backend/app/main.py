import json
import sqlite3
from pathlib import Path

from fastapi import FastAPI
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


class PhysicalItem(BaseModel):
    id: int | None = None
    barcode: str | None = None
    title: str
    year: int | None = None
    media_type: str = "bluray"
    edition_label: str | None = None
    original_location: str | None = None
    current_state: str = "in_stock"
    temporary_holder: str | None = None

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


app = FastAPI(title="Avatra", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def encode_list_metadata(value: list[str] | None) -> str:
    return json.dumps(value or [])


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
                current_state TEXT NOT NULL DEFAULT 'in_stock',
                temporary_holder TEXT,
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
                discs INTEGER
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


@app.get("/items")
def list_items():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM physical_items ORDER BY id DESC").fetchall()
        return [dict(row) for row in rows]


@app.post("/items")
def create_item(item: PhysicalItem):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO physical_items (
                barcode, title, year, media_type, edition_label,
                original_location, current_state, temporary_holder,
                resolution, video_codec, hdr, aspect_ratio,
                original_aspect_ratio, audio_tracks, spoken_languages,
                subtitles, region, runtime, discs
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.barcode,
                item.title,
                item.year,
                item.media_type,
                item.edition_label,
                item.original_location,
                item.current_state,
                item.temporary_holder,
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
            ),
        )
        conn.commit()
        item.id = cursor.lastrowid
        return item
    
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
