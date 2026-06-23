from app.lookup.providers import SearchResult
from app.lookup.consensus import choose_best


def lookup(barcode: str):

    # TODO : remplacer par les vrais providers
    results = [
        SearchResult(
            source="DVDfr",
            title="La Collection des Courts Métrages Pixar - Volume 2",
            url="https://www.dvdfr.com/",
            score=10,
        ),
        SearchResult(
            source="Fnac",
            title="La Collection des Courts Métrages Pixar - Volume 2",
            url="https://www.fnac.com/",
            score=8,
        ),
        SearchResult(
            source="Amazon",
            title="Pixar Short Films Collection Volume 2",
            url="https://www.amazon.fr/",
            score=6,
        ),
    ]

    return choose_best(results)
