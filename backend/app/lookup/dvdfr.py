import re
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

from app.lookup.providers import SearchResult


def clean_dvdfr_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"\s*-\s*Blu-ray\s*$", "", title, flags=re.I)
    title = re.sub(r"\s*\[Blu-ray\]\s*$", "", title, flags=re.I)
    return title.strip()


async def search_dvdfr(barcode: str) -> list[SearchResult]:
    url = (
        "https://www.dvdfr.com/search/multisearch.php"
        f"?multiname={quote_plus(barcode)}&x=29&y=10"
    )

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
        )

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    candidates: list[SearchResult] = []

    for link in soup.find_all("a"):
        title = link.get_text(" ", strip=True)
        href = link.get("href") or ""

        if not title:
            continue

        if barcode not in page_text:
            continue

        if "blu-ray" not in title.lower() and "dvd" not in title.lower():
            continue

        candidates.append(
            SearchResult(
                source="DVDfr",
                title=clean_dvdfr_title(title),
                url=href,
                score=10,
            )
        )

    # Fallback : si le titre est dans le <title> HTML
    if not candidates:
        html_title = soup.title.get_text(" ", strip=True) if soup.title else ""
        if barcode in page_text and html_title:
            candidates.append(
                SearchResult(
                    source="DVDfr",
                    title=clean_dvdfr_title(html_title),
                    url=url,
                    score=8,
                )
            )

    return candidates[:5]
