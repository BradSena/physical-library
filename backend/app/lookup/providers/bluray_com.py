import re
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup
from bs4.element import NavigableString, PageElement, Tag

from app.lookup.models import DiscMetadata, RecognitionProvider


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title or "").strip()
    title = re.sub(r"\s*Blu-ray\s*$", "", title, flags=re.IGNORECASE).strip()
    return title


def extract_year(text: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(match.group(0)) if match else None


def media_type_from_text(*values: str | None) -> str | None:
    text = " ".join(value or "" for value in values).lower()
    text = (text or "").lower()
    if "4k" in text or "ultra hd" in text or "uhd" in text:
        return "uhd"
    if "blu-ray" in text or "bluray" in text:
        return "bluray"
    if "dvd" in text:
        return "dvd"
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


def clean_value(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" :")


def section_heading_text(element: PageElement) -> str:
    if not isinstance(element, Tag):
        return ""

    classes = element.get("class") or []
    if element.name != "span" or "subheading" not in classes:
        return ""

    return clean_value(element.get_text(" ", strip=True)).lower()


def extract_section_lines(soup: BeautifulSoup, heading: str) -> list[str]:
    expected_heading = heading.lower()

    for subheading in soup.select("span.subheading"):
        if section_heading_text(subheading) != expected_heading:
            continue

        parts: list[str] = []
        for sibling in subheading.next_siblings:
            if section_heading_text(sibling):
                break

            if isinstance(sibling, NavigableString):
                parts.append(str(sibling))
                continue

            if not isinstance(sibling, Tag):
                continue

            if sibling.name == "br":
                parts.append("\n")
                continue

            if sibling.get("id") in {"longaudio", "longsubs"}:
                continue

            parts.append(sibling.get_text("\n", strip=True))

        text = "".join(parts)
        return [
            clean_value(line)
            for line in text.splitlines()
            if clean_value(line)
        ]

    return []


def extract_labeled_value(lines: list[str], label: str) -> str | None:
    expected_label = label.lower()

    for line in lines:
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        if clean_value(key).lower() == expected_label:
            return clean_value(value) or None

    return None


def extract_runtime(text: str | None) -> int | None:
    match = re.search(r"\b(\d{1,3})\s*min(?:ute)?s?\b", text or "", re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_structured_runtime(soup: BeautifulSoup) -> int | None:
    runtime = soup.select_one("#runtime")
    if not runtime:
        return None

    return extract_runtime(runtime.get_text(" ", strip=True))


def extract_discs(lines: list[str]) -> int | None:
    text = " ".join(lines)
    match = re.search(r"\b(\d{1,2})\s*disc(?:s)?\b", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    match = re.search(r"\b(\d{1,2})-disc(?:s)?\b", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    word_counts = {
        "single": 1,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    match = re.search(r"\b([a-z]+)-disc(?:s)?\b", text, re.IGNORECASE)
    if match:
        return word_counts.get(match.group(1).lower())

    return None


def extract_region(lines: list[str]) -> str | None:
    regions: list[str] = []

    for line in lines:
        match = re.search(r"\bRegion\s+([A-C]|Free|All)\b", line, re.IGNORECASE)
        if not match:
            continue

        region = match.group(1)
        regions.append(region.upper() if len(region) == 1 else region.title())

    if not regions:
        return None

    return ", ".join(dict.fromkeys(regions))


def split_list(value: str | None) -> list[str]:
    if not value:
        return []

    values = re.split(r",|/", value)
    return [
        clean_value(item)
        for item in values
        if clean_value(item)
    ]


def extract_audio_tracks(lines: list[str]) -> list[str]:
    return [
        line
        for line in lines
        if ":" in line and not line.lower().startswith("audio descriptive")
    ]


def extract_spoken_languages(audio_tracks: list[str]) -> list[str]:
    languages: list[str] = []

    for track in audio_tracks:
        language = clean_value(track.split(":", 1)[0])
        if language:
            languages.append(language)

    return list(dict.fromkeys(languages))


def extract_subtitles(lines: list[str]) -> list[str]:
    subtitles: list[str] = []

    for line in lines:
        subtitles.extend(split_list(line))

    return list(dict.fromkeys(subtitles))


def extract_edition_label(soup: BeautifulSoup) -> str | None:
    label = soup.select_one("span.subheadingtitle")
    if not label:
        return None

    return clean_value(label.get_text(" ", strip=True)) or None


def extract_structured_year(soup: BeautifulSoup) -> int | None:
    for label in soup.select("span.subheading.grey"):
        year = extract_year(label.get_text(" ", strip=True))
        if year:
            return year

    return None


def strip_codec_bitrate(value: str | None) -> str | None:
    if not value:
        return None

    return clean_value(re.sub(r"\s*\([^)]*\)\s*$", "", value))


async def fetch_detail(client: httpx.AsyncClient, url: str, barcode: str) -> DiscMetadata | None:
    response = await client.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 Avatra/0.1"},
    )

    if response.status_code != 200:
        return None

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    title = extract_title(soup)
    if not title:
        return None

    edition_label = extract_edition_label(soup)
    video_lines = extract_section_lines(soup, "Video")
    audio_lines = extract_section_lines(soup, "Audio")
    subtitle_lines = extract_section_lines(soup, "Subtitles")
    disc_lines = extract_section_lines(soup, "Discs")
    playback_lines = extract_section_lines(soup, "Playback")

    video_codec = strip_codec_bitrate(extract_labeled_value(video_lines, "Codec"))
    audio_tracks = extract_audio_tracks(audio_lines)

    return DiscMetadata(
        source="Blu-ray.com",
        barcode=barcode,
        title=title,
        year=extract_structured_year(soup) or extract_year(edition_label or title),
        media_type=media_type_from_text(title, edition_label, " ".join(disc_lines)),
        edition_label=edition_label,
        resolution=extract_labeled_value(video_lines, "Resolution"),
        video_codec=video_codec,
        hdr=split_list(extract_labeled_value(video_lines, "HDR")),
        aspect_ratio=extract_labeled_value(video_lines, "Aspect ratio"),
        original_aspect_ratio=extract_labeled_value(video_lines, "Original aspect ratio"),
        audio_tracks=audio_tracks,
        spoken_languages=extract_spoken_languages(audio_tracks),
        subtitles=extract_subtitles(subtitle_lines),
        region=extract_region(playback_lines),
        runtime=extract_structured_runtime(soup),
        discs=extract_discs(disc_lines),
        url=url,
        score=10,
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
