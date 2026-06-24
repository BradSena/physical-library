import re
from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.lookup.providers import SearchResult


def clean_dvdfr_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    return title


def looks_like_disc_result(title: str, href: str) -> bool:
    if not title or not href:
        return False

    if not href.startswith("/dvd/"):
        return False

    if len(title.strip()) < 8:
        return False

    if "€" in title or "blu-ray" == title.strip().lower() or title.strip().lower() == "dvd":
        return False

    return True


async def search_dvdfr(barcode: str) -> list[SearchResult]:
    url = (
    "https://www.dvdfr.com/listeliv.php"
    f"?base=dvd&mots_recherche={quote_plus(barcode)}"
    )

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
        )

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    candidates: list[SearchResult] = []

    for link in soup.find_all("a"):
        title = link.get_text(" ", strip=True)
        href = link.get("href") or ""

        if not looks_like_disc_result(title, href):
            continue

        candidates.append(
            SearchResult(
                source="DVDfr",
                title=clean_dvdfr_title(title),
                url=urljoin("https://www.dvdfr.com/", href),
                score=10,
            )
        )
    print("DVDfr candidates:", candidates)

    return candidates[:5]
