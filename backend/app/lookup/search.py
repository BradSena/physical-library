from app.lookup.consensus import choose_best
from app.lookup.dvdfr import search_dvdfr


async def lookup(barcode: str):
    results = []
    results.extend(await search_dvdfr(barcode))
    return choose_best(results)
