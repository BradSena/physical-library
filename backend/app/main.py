from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


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


app = FastAPI(
    title="Avatra",
    version="0.1.0",
)

items: list[PhysicalItem] = []

app.mount("/static", StaticFiles(directory="app/static"), name="static")


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


@app.get("/items")
def list_items():
    return items


@app.post("/items")
def create_item(item: PhysicalItem):
    item.id = len(items) + 1
    items.append(item)
    return item