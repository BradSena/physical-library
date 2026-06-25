from app.lookup.consensus import choose_best
from app.lookup.providers.dvdfr import search_dvdfr


async def lookup(barcode: str):
    results = []
    results.extend(await search_dvdfr(barcode))
    return choose_best(results)
