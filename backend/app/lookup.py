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

async def lookup_eansearch(barcode: str):
    url = f"https://api.ean-search.org/api?op=barcode-lookup&format=json&ean={barcode}"

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(url)

        if r.status_code != 200:
            return None

        data = r.json()

        if not data:
            return None

        title = data.get("name") or data.get("productname")
        if not title:
            return None

        return {
            "barcode": barcode,
            "title": clean_title(title),
            "year": extract_year(title),
            "media_type": guess_media_type(title),
        }

    except Exception:
        return None

async def lookup_barcode(barcode: str) -> dict:
    # 1. UPCItemDB
    result = await lookup_upcitemdb(barcode)
    if result:
        result["source"] = "UPCItemDB"
        result["confidence"] = 0.75
        return {
            "found": True,
            "result": result,
            "candidates": [result],
        }

    # 2. EAN-Search
    result = await lookup_eansearch(barcode)
    if result:
        result["source"] = "EAN-Search"
        result["confidence"] = 0.85
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
        "message": "Barcode not recognized.",
    }