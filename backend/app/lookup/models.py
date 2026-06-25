from abc import ABC, abstractmethod
from pydantic import BaseModel


class SearchResult(BaseModel):
    source: str
    title: str
    url: str | None = None
    score: int = 0
    year: int | None = None
    media_type: str | None = None


class RecognitionProvider(ABC):
    name: str

    @abstractmethod
    async def search(self, barcode: str) -> list[SearchResult]:
        ...