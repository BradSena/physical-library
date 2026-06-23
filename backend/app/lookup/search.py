from app.lookup.consensus import choose_best
from app.lookup.searx import search_searx


async def lookup(barcode: str):
    results = await search_searx(barcode)
    return choose_best(results)
