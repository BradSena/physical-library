from app.lookup.models import RecognitionProvider, SearchResult
import re
from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.lookup.models import SearchResult


def fix_mojibake(text: str) -> str:
    replacements = {
        "Ã©": "é", "Ã¨": "è", "Ãª": "ê", "Ã ": "à",
        "Ã¢": "â", "Ã§": "ç", "Ã´": "ô", "Ã»": "û",
        "Ã®": "î", "Ã¯": "ï", "â‚¬": "€",
    }
    for bad, good in replacements.items():
        text = (text or "").replace(bad, good)
    return text


def extract_year(title: str) -> int | None:
    match = re.search(r"\((19|20)\d{2}\)", title or "")
    return int(match.group(0).strip("()")) if match else None


def clean_dvdfr_title(title: str) -> str:
    title = fix_mojibake(title)
    title = re.sub(r"\((19|20)\d{2}\)", "", title)
    title = re.sub(r"\s+", " ", title or "").strip()
    return title


def media_type_from_detail_title(text: str) -> str:
    text = (text or "").lower()
    if "4k" in text or "ultra hd" in text or "uhd" in text:
        return "uhd"
    if "blu-ray" in text or "bluray" in text:
        return "bluray"
    if "dvd" in text:
        return "dvd"
    return "bluray"


def looks_like_disc_result(title: str, href: str) -> bool:
    if not title or not href:
        return False
    if not href.startswith("/dvd/"):
        return False
    clean = title.strip().lower()
    if len(clean) < 8:
        return False
    if "€" in clean:
        return False
    if clean in {"blu-ray", "blu-ray 3d", "dvd", "hd dvd"}:
        return False
    return True


async def enrich_from_detail(client: httpx.AsyncClient, href: str, fallback_year: int | None):
    detail_url = urljoin("https://www.dvdfr.com/", href)

    try:
        response = await client.get(
            detail_url,
            headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
        )
    except Exception:
        return fallback_year, "bluray"

    if response.status_code != 200:
        return fallback_year, "bluray"

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    detail_title = soup.title.get_text(" ", strip=True) if soup.title else ""
    media_type = media_type_from_detail_title(detail_title)

    year = fallback_year
    if year is None:
        year_tag = soup.select_one(".commentLangue")
        if year_tag:
            year = extract_year(year_tag.get_text(" ", strip=True))

    if year is None:
        match = re.search(r'"releaseDate"\s*:\s*"(\d{2})/(\d{2})/((19|20)\d{2})"', response.text)
        if match:
            year = int(match.group(3))

    return year, media_type


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

        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        candidates: list[SearchResult] = []

        for link in soup.find_all("a"):
            raw_title = link.get_text(" ", strip=True)
            href = link.get("href") or ""

            if not looks_like_disc_result(raw_title, href):
                continue

            year = extract_year(raw_title)
            year, media_type = await enrich_from_detail(client, href, year)

            candidates.append(
                SearchResult(
                    source="DVDfr",
                    title=clean_dvdfr_title(raw_title),
                    url=urljoin("https://www.dvdfr.com/", href),
                    score=10,
                    year=year,
                    media_type=media_type,
                )
            )

    return candidates[:5]

class DVDfrProvider(RecognitionProvider):
    name = "DVDfr"

    async def search(self, barcode: str):
        return await search_dvdfr(barcode)
