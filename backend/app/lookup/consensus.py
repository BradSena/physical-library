from app.lookup.models import DiscMetadata


def fix_mojibake(text: str | None) -> str | None:
    if not text:
        return text

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


def choose_best(results: list[DiscMetadata]) -> dict:
    if not results:
        return {
            "found": False,
            "result": None,
            "candidates": [],
        }

    sorted_results = sorted(results, key=lambda r: r.score, reverse=True)
    merged = DiscMetadata(source="merged", score=sum(r.score for r in results))

    for result in sorted_results:
        if not merged.barcode and result.barcode:
            merged.barcode = result.barcode

        if not merged.title and result.title:
            merged.title = fix_mojibake(result.title)

        if not merged.original_title and result.original_title:
            merged.original_title = fix_mojibake(result.original_title)

        if not merged.year and result.year:
            merged.year = result.year

        if not merged.media_type and result.media_type:
            merged.media_type = result.media_type

        if not merged.edition_label and result.edition_label:
            merged.edition_label = result.edition_label

        if not merged.country and result.country:
            merged.country = result.country

        if not merged.resolution and result.resolution:
            merged.resolution = result.resolution

        if not merged.video_codec and result.video_codec:
            merged.video_codec = result.video_codec

        if not merged.aspect_ratio and result.aspect_ratio:
            merged.aspect_ratio = result.aspect_ratio

        if not merged.original_aspect_ratio and result.original_aspect_ratio:
            merged.original_aspect_ratio = result.original_aspect_ratio

        if not merged.region and result.region:
            merged.region = result.region

        if not merged.runtime and result.runtime:
            merged.runtime = result.runtime

        if not merged.discs and result.discs:
            merged.discs = result.discs

        if not merged.url and result.url:
            merged.url = result.url

        for value in result.hdr:
            if value not in merged.hdr:
                merged.hdr.append(value)

        for value in result.audio_tracks:
            if value not in merged.audio_tracks:
                merged.audio_tracks.append(value)

        for value in result.spoken_languages:
            if value not in merged.spoken_languages:
                merged.spoken_languages.append(value)

        for value in result.subtitles:
            if value not in merged.subtitles:
                merged.subtitles.append(value)

    return {
        "found": bool(merged.title),
        "result": merged.model_dump(),
        "candidates": [
            result.model_dump()
            for result in sorted_results
        ],
    }
