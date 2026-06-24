from dataclasses import dataclass


@dataclass
class SearchResult:
    source: str
    title: str
    url: str
    score: int = 1
    year: int | None = None
    media_type: str | None = None
