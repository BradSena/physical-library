from collections import defaultdict

from app.lookup.models import SearchResult


def fix_mojibake(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "mÃ©": "mé",
        "Ã©": "é",
        "Ã¨": "è",
        "Ãª": "ê",
        "Ã ": "à",
        "Ã¢": "â",
        "Ã§": "ç",
        "Ã´": "ô",
        "Ã»": "û",
        "Ã®": "î",
        "Ã¯": "ï",
        "â‚¬": "€",
    }

    for bad, good in replacements.items():
        text = text.replace(bad, good)

    return text


def choose_best(results: list[SearchResult]) -> dict:
    votes: dict[str, int] = defaultdict(int)
    metadata: dict[str, dict] = {}

    for result in results:
        title = fix_mojibake(result.title)
        votes[title] += result.score

        metadata.setdefault(title, {
            "year": result.year,
            "media_type": result.media_type,
        })

    if not votes:
        return {
            "found": False,
            "result": None,
            "candidates": [],
        }

    best_title = max(votes, key=votes.get)
    best_score = votes[best_title]
    best_metadata = metadata.get(best_title, {})

    return {
        "found": True,
        "result": {
            "title": best_title,
            "confidence": best_score,
            "year": best_metadata.get("year"),
            "media_type": best_metadata.get("media_type") or "bluray",
        },
        "candidates": [
            {
                "title": title,
                "score": score,
                "year": metadata.get(title, {}).get("year"),
                "media_type": metadata.get(title, {}).get("media_type"),
            }
            for title, score in sorted(
                votes.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
    }
