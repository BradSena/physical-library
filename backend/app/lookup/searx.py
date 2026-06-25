import httpx

from app.lookup.models import SearchResult


SEARX_INSTANCE = "https://search.inetol.net"


def site_weight(url: str) -> int:
    url = url.lower()

    if "dvdfr.com" in url:
        return 10
    if "blu-ray.com" in url:
        return 10
    if "fnac.com" in url:
        return 8
    if "e.leclerc" in url:
        return 7
    if "amazon." in url:
        return 7
    if "chasse-aux-livres.fr" in url:
        return 6
    if "momox" in url:
        return 5
    if "rakuten" in url:
        return 5

    return 3


async def search_searx(barcode: str) -> list[SearchResult]:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{SEARX_INSTANCE}/search",
            params={
                "q": barcode,
                "format": "json",
                "language": "fr",
                "categories": "general",
            },
            headers={"User-Agent": "Avatra/0.1"},
        )

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for item in data.get("results", [])[:10]:
        title = item.get("title")
        url = item.get("url", "")

        if not title:
            continue

        results.append(
            SearchResult(
                source=url,
                title=title,
                url=url,
                score=site_weight(url),
            )
        )

    return results
