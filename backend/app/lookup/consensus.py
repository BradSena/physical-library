from collections import defaultdict

from app.lookup.providers import SearchResult


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

    for result in results:
        title = fix_mojibake(result.title)
        votes[title] += result.score

    if not votes:
        return {
            "found": False,
            "result": None,
            "candidates": [],
        }

    best_title = max(votes, key=votes.get)
    best_score = votes[best_title]

    return {
        "found": True,
        "result": {
            "title": best_title,
            "confidence": best_score,
        },
        "candidates": [
            {"title": title, "score": score}
            for title, score in sorted(
                votes.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ],
    }
