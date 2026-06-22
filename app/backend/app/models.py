from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field

class DiscStatus(str, Enum):
    stock = "stock"
    loaned = "loaned"
    expo = "expo"
    missing = "missing"

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: Optional[int] = None
    barcode: Optional[str] = Field(default=None, index=True)
    support: str = "Blu-ray"
    original_location: str = Field(index=True)
    current_status: DiscStatus = DiscStatus.stock
    current_holder: Optional[str] = None
    expo_location: Optional[str] = None
    tmdb_id: Optional[int] = Field(default=None, index=True)
    imdb_id: Optional[str] = None
    edition_label: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ScanCandidate(SQLModel):
    source: str
    confidence: float
    title: str
    year: Optional[int] = None
    support: Optional[str] = None
    tmdb_id: Optional[int] = None
    imdb_id: Optional[str] = None
    raw_name: Optional[str] = None

class ScanResult(SQLModel):
    barcode: str
    candidates: list[ScanCandidate]
    best: Optional[ScanCandidate] = None
    needs_manual: bool = True

class CreateMovie(SQLModel):
    title: str
    year: Optional[int] = None
    barcode: Optional[str] = None
    support: str = "Blu-ray"
    original_location: str
    tmdb_id: Optional[int] = None
    imdb_id: Optional[str] = None
    edition_label: Optional[str] = None

class MoveMovie(SQLModel):
    status: DiscStatus
    holder: Optional[str] = None
    expo_location: Optional[str] = None
