import re
import httpx


def extract_year(text: str) -> int | None:
    match = re.search(r"\b(19|20)\d{2}\b", text or "")
    return int(match.group(0)) if match else None


def clean_title(title: str) -> str:
    if not title:
        return ""
    title = re.sub(r"\b(Blu[- ]?ray|DVD|UHD|4K|Ultra HD|Steelbook)\b", "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title)
    return title.strip(" -:|")


async def lookup_upcitemdb(barcode: str) -> dict | None:
    url = "https://api.upcitemdb.com/prod/trial/lookup"
    async with httpx.AsyncClient(timeout=8) as client:
        response = await client.get(url, params={"upc": barcode})
        response.raise_for_status()
        data = response.json()

    items = data.get("items") or []
    if not items:
        return None

    item = items[0]
    raw_title = item.get("title") or ""
    title = clean_title(raw_title)
    year = extract_year(raw_title)

    return {
        "barcode": barcode,
        "title": title or raw_title,
        "year": year,
        "media_type": guess_media_type(raw_title),
        "source": "upcitemdb",
        "confidence": 0.75,
        "raw_title": raw_title,
    }


def guess_media_type(text: str) -> str:
    text = (text or "").lower()
    if "uhd" in text or "4k" in text or "ultra hd" in text:
        return "uhd"
    if "dvd" in text:
        return "dvd"
    return "bluray"


async def lookup_barcode(barcode: str) -> dict:
    result = await lookup_upcitemdb(barcode)

    if result:
        return {
            "found": True,
            "result": result,
            "candidates": [result],
        }

    return {
        "found": False,
        "result": None,
        "candidates": [],
        "manual_required": True,
        "message": "Barcode not recognized. Manual entry required.",
    }
