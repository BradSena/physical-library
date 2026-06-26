import re
from urllib.parse import quote_plus, urljoin

import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.lookup.models import DiscMetadata, RecognitionProvider


BASE_URL = "https://www.blu-ray.com/"


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"\s*Blu-ray\s*$", "", title, flags=re.IGNORECASE).strip()
    return title


def extract_year(text: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(match.group(0)) if match else None


def media_type_from_text(text: str) -> str | None:
    text = (text or "").lower()
    if "4k" in text or "ultra hd" in text or "uhd" in text:
        return "uhd"
    if "blu-ray" in text or "bluray" in text:
        return "bluray"
    if "dvd" in text:
        return "dvd"
    return None


def looks_like_bluray_movie_link(title: str, href: str) -> bool:
    if not title or not href:
        return False

    if "/movies/" not in href:
        return False

    if not re.search(r"/movies/.+/\d+/?$", href):
        return False

    clean = title.strip().lower()

    if len(clean) < 4:
        return False

    if clean in {"blu-ray", "4k ultra hd", "dvd"}:
        return False

    return True


def find_search_results_container(soup: BeautifulSoup) -> Tag | None:
    for selector in [
        "#searchresults",
        ".searchresults",
    ]:
        container = soup.select_one(selector)
        if isinstance(container, Tag):
            return container

    for header in soup.select("div.boxheader"):
        header_text = header.get_text(" ", strip=True).lower()
        if "search" not in header_text or "result" not in header_text:
            continue

        table = header.find_next_sibling("table")
        if isinstance(table, Tag):
            return table

    return None


def extract_meta_content(soup: BeautifulSoup, selector: str) -> str | None:
    tag = soup.select_one(selector)
    if not tag:
        return None

    content = tag.get("content")
    if not content:
        return None

    return str(content).strip() or None


def extract_title(soup: BeautifulSoup) -> str | None:
    for selector in [
        'meta[property="og:title"]',
        'meta[name="twitter:title"]',
    ]:
        title = extract_meta_content(soup, selector)
        if title:
            return clean_title(title)

    heading = soup.find("h1")
    if heading:
        title = clean_title(heading.get_text(" ", strip=True))
        if title:
            return title

    if soup.title:
        title = clean_title(soup.title.get_text(" ", strip=True))
        title = re.sub(r"\s*- Blu-ray\.com\s*$", "", title).strip()
        if title:
            return title

    return None


def extract_runtime(text: str) -> int | None:
    match = re.search(r"\b(\d{1,3})\s*min(?:ute)?s?\b", text or "", re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_discs(text: str) -> int | None:
    match = re.search(r"\b(\d{1,2})\s*disc(?:s)?\b", text or "", re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_region(text: str) -> str | None:
    match = re.search(r"\bRegion\s+([A-C]|Free|All)\b", text or "", re.IGNORECASE)
    if not match:
        return None

    region = match.group(1)
    return region.upper() if len(region) == 1 else region.title()


def extract_country(text: str) -> str | None:
    match = re.search(r"\bCountry\s+([A-Za-z][A-Za-z\s]+?)(?:\s{2,}|Release|Studio|UPC|$)", text or "")
    if not match:
        return None

    return match.group(1).strip() or None


async def fetch_detail(client: httpx.AsyncClient, url: str, barcode: str) -> DiscMetadata | None:
    response = await client.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
    )

    if response.status_code != 200:
        return None

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(" ", strip=True)

    title = extract_title(soup)
    if not title:
        return None

    return DiscMetadata(
        source="Blu-ray.com",
        barcode=barcode,
        title=title,
        year=extract_year(page_text),
        media_type=media_type_from_text(page_text),
        country=extract_country(page_text),
        region=extract_region(page_text),
        runtime=extract_runtime(page_text),
        discs=extract_discs(page_text),
        url=url,
        score=10 if barcode in page_text else 6,
    )


async def search_bluray_com(barcode: str) -> list[DiscMetadata]:
    search_url = (
        "https://www.blu-ray.com/search/"
        "?quicksearch=1"
        "&quicksearch_country=all"
        f"&quicksearch_keyword={quote_plus(barcode)}"
        "&section=bluraymovies"
    )

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        response = await client.get(
            search_url,
            headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
        )

        final_url = str(response.url)

        if response.status_code != 200:
            return []

        if "/movies/" not in final_url:
            return []

        metadata = await fetch_detail(client, final_url, barcode)

        return [metadata] if metadata else []


class BluRayComProvider(RecognitionProvider):
    name = "Blu-ray.com"

    async def search(self, barcode: str) -> list[DiscMetadata]:
        return await search_bluray_com(barcode)
