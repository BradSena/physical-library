from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class MediaType(str, Enum):
    dvd = "dvd"
    bluray = "bluray"
    uhd = "uhd"


class ItemState(str, Enum):
    in_stock = "in_stock"
    on_display = "on_display"
    on_loan = "on_loan"
    missing = "missing"


class PhysicalItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    barcode: Optional[str] = Field(default=None, index=True)
    title: str
    year: Optional[int] = None
    media_type: MediaType = MediaType.bluray
    edition_label: Optional[str] = None
    original_location: Optional[str] = None
    current_state: ItemState = ItemState.in_stock
    temporary_holder: Optional[str] = None