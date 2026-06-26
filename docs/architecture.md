# Avatra Architecture

Avatra is the physical media layer for Kodi.

Kodi remains responsible for the movie experience: posters, fanart, synopsis, actors, collections, browsing and playback UI.

Avatra is responsible for the physical reality of the collection: disc ownership, edition identification, storage location, availability, technical disc metadata and automation.

---

## Core Principle

Kodi knows the movie.

Avatra knows the disc.

---

## High-Level Architecture

```text
                Kodi
                 ▲
                 │
          Kodi Avatra Add-on
                 ▲
                 │
              REST API
                 ▲
                 │
┌────────────────────────────────────┐
│              Avatra                │
├────────────────────────────────────┤
│ Recognition Engine                 │
│ Collection Manager                 │
│ Shelf Map                          │
│ Kodi Exporter                      │
│ Automation Bridge                  │
└────────────────────────────────────┘
       ▲                       ▲
       │                       │
Metadata Providers        Home Assistant
DVDfr, Blu-ray.com...     ESPHome, LEDs, AVR...

Puis :

```bash
git add .gitignore docs/architecture.md
git commit -m "docs: add architecture overview"
git push
cat > app/lookup/cede.py <<'EOF'
import re
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup

from app.lookup.providers import SearchResult


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"\s*[-|].*$", "", title).strip()
    return title


def extract_year(text: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(match.group(0)) if match else None


def media_type_from_text(text: str) -> str | None:
    text = (text or "").lower()
    if "4k" in text or "uhd" in text or "ultra hd" in text:
        return "uhd"
    if "blu-ray" in text or "bluray" in text:
        return "bluray"
    if "dvd" in text:
        return "dvd"
    return None


async def search_cede(barcode: str) -> list[SearchResult]:
    url = f"https://www.cede.ch/en/search/?q={quote_plus(barcode)}"

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
        )

    if response.status_code != 200:
        return []

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    if barcode not in page_text:
        return []

    html_title = soup.title.get_text(" ", strip=True) if soup.title else ""
    title = clean_title(html_title)

    if not title:
        h1 = soup.find("h1")
        title = clean_title(h1.get_text(" ", strip=True)) if h1 else ""

    if not title:
        return []

    return [
        SearchResult(
            source="CeDe",
            title=title,
            url=str(response.url),
            score=7,
            year=extract_year(page_text),
            media_type=media_type_from_text(page_text),
        )
    ]
