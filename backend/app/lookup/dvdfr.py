import re
from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup

from app.lookup.providers import SearchResult


def fix_mojibake(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "Ã©": "é",
        "Ã¨": "è",
        "Ãª": "ê",
        "Ã ": "à",
        "Ã¢": "â",
        "Ã§": "ç",
        "Ã´": "ô",
        "Ã»": "û",
        "Ã®": "î",
        "Ã¯": "ï",
        "â‚¬": "€",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text


def clean_dvdfr_title(title: str) -> str:
    title = fix_mojibake(title)
    title = re.sub(r"\s+", " ", title or "").strip()
    return title


def looks_like_disc_result(title: str, href: str) -> bool:
    if not title or not href:
        return False

    if not href.startswith("/dvd/"):
        return False

    clean_title = title.strip().lower()

    if len(clean_title) < 8:
        return False

    if "€" in clean_title:
        return False

    if clean_title in {"blu-ray", "blu-ray 3d", "dvd", "hd dvd"}:
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

    response.encoding = "utf-8"
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

    return candidates[:5]
