import os, re
from typing import Optional
import httpx
from .models import ScanCandidate, ScanResult

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
UPCITEMDB_API_KEY = os.getenv("UPCITEMDB_API_KEY", "")
BARCODELOOKUP_API_KEY = os.getenv("BARCODELOOKUP_API_KEY", "")

MOVIE_HINTS = ["blu-ray", "bluray", "dvd", "uhd", "4k", "steelbook", "movie", "film"]
NOISE = ["blu-ray", "bluray", "dvd", "uhd", "4k", "steelbook", "edition", "collector", "disc", "movie"]

def clean_title(name: str) -> str:
    value = name or ""
    value = re.sub(r"\([^)]*\)", " ", value)
    for word in NOISE:
        value = re.sub(rf"\b{re.escape(word)}\b", " ", value, flags=re.I)
    value = re.sub(r"\s+", " ", value).strip(" -–|:")
    return value.strip()

def detect_support(name: str) -> Optional[str]:
    n = (name or "").lower()
    if "4k" in n or "uhd" in n:
        return "UHD Blu-ray"
    if "blu" in n:
        return "Blu-ray"
    if "dvd" in n:
        return "DVD"
    return None

async def tmdb_search(title: str, year: Optional[int] = None) -> Optional[ScanCandidate]:
    if not TMDB_API_KEY or not title:
        return None
    params = {"api_key": TMDB_API_KEY, "query": title, "language": "fr-FR"}
    if year:
        params["year"] = year
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://api.themoviedb.org/3/search/movie", params=params)
        if r.status_code != 200:
            return None
        data = r.json()
    results = data.get("results", [])
    if not results:
        return None
    first = results[0]
    release = first.get("release_date") or ""
    found_year = int(release[:4]) if release[:4].isdigit() else year
    # crude confidence: first TMDb hit from a cleaned barcode product title
    return ScanCandidate(source="tmdb", confidence=0.72, title=first.get("title") or title, year=found_year, tmdb_id=first.get("id"), raw_name=title)

async def lookup_upcitemdb(barcode: str) -> list[ScanCandidate]:
    headers = {}
    if UPCITEMDB_API_KEY:
        headers["user_key"] = UPCITEMDB_API_KEY
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}" if not UPCITEMDB_API_KEY else f"https://api.upcitemdb.com/prod/v1/lookup?upc={barcode}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers=headers)
        if r.status_code != 200:
            return []
        items = r.json().get("items", [])
    except Exception:
        return []
    out = []
    for item in items[:3]:
        raw = item.get("title") or ""
        title = clean_title(raw)
        support = detect_support(raw)
        conf = 0.55 + (0.15 if support else 0) + (0.10 if any(h in raw.lower() for h in MOVIE_HINTS) else 0)
        out.append(ScanCandidate(source="upcitemdb", confidence=min(conf, .85), title=title or raw, support=support, raw_name=raw))
    return out

async def lookup_barcodelookup(barcode: str) -> list[ScanCandidate]:
    if not BARCODELOOKUP_API_KEY:
        return []
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.barcodelookup.com/v3/products", params={"barcode": barcode, "formatted": "y", "key": BARCODELOOKUP_API_KEY})
        if r.status_code != 200:
            return []
        products = r.json().get("products", [])
    except Exception:
        return []
    out = []
    for p in products[:3]:
        raw = p.get("title") or ""
        title = clean_title(raw)
        support = detect_support(raw)
        conf = 0.58 + (0.15 if support else 0)
        out.append(ScanCandidate(source="barcodelookup", confidence=min(conf, .85), title=title or raw, support=support, raw_name=raw))
    return out

async def resolve_barcode(barcode: str) -> ScanResult:
    candidates: list[ScanCandidate] = []
    candidates += await lookup_upcitemdb(barcode)
    candidates += await lookup_barcodelookup(barcode)

    enriched: list[ScanCandidate] = []
    for c in candidates:
        tmdb = await tmdb_search(c.title)
        if tmdb:
            tmdb.source = c.source + "+tmdb"
            tmdb.confidence = min(c.confidence + 0.12, 0.95)
            tmdb.support = c.support
            tmdb.raw_name = c.raw_name
            enriched.append(tmdb)
        else:
            enriched.append(c)
    enriched.sort(key=lambda x: x.confidence, reverse=True)
    best = enriched[0] if enriched else None
    return ScanResult(barcode=barcode, candidates=enriched, best=best, needs_manual=(best is None or best.confidence < 0.80))
