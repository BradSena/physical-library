from dataclasses import dataclass


@dataclass
class SearchResult:
    source: str
    title: str
    url: str
    score: int = 1
