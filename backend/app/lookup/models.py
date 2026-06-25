from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class DiscMetadata(BaseModel):
    source: str

    # Identification
    barcode: str | None = None
    title: str | None = None
    original_title: str | None = None
    year: int | None = None

    # Edition
    media_type: str | None = None
    edition_label: str | None = None
    country: str | None = None

    # Video
    resolution: str | None = None
    video_codec: str | None = None
    hdr: list[str] = Field(default_factory=list)
    aspect_ratio: str | None = None
    original_aspect_ratio: str | None = None

    # Audio
    audio_tracks: list[str] = Field(default_factory=list)

    # Languages
    spoken_languages: list[str] = Field(default_factory=list)
    subtitles: list[str] = Field(default_factory=list)

    # Disc
    region: str | None = None
    runtime: int | None = None
    discs: int | None = None

    # Provider metadata
    score: int = 0
    url: str | None = None


# Temporary compatibility alias while providers are migrated
SearchResult = DiscMetadata


class RecognitionProvider(ABC):
    name: str

    @abstractmethod
    async def search(self, barcode: str) -> list[DiscMetadata]:
        ...
