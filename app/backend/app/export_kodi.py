import os, re
from pathlib import Path
from slugify import slugify
from .models import Movie

EXPORT_ROOT = os.getenv("EXPORT_ROOT", "/exports/kodi")
KODI_PLUGIN_URL = os.getenv("KODI_PLUGIN_URL", "plugin://plugin.video.physicaldisc/play?movie_id={movie_id}")

def safe_folder(movie: Movie) -> str:
    year = f" ({movie.year})" if movie.year else ""
    name = re.sub(r"[\\/:*?\"<>|]", " ", f"{movie.title}{year}")
    return re.sub(r"\s+", " ", name).strip()

def export_movie(movie: Movie) -> Path:
    root = Path(EXPORT_ROOT)
    folder = root / safe_folder(movie)
    folder.mkdir(parents=True, exist_ok=True)
    strm = folder / f"{safe_folder(movie)}.strm"
    strm.write_text(KODI_PLUGIN_URL.format(movie_id=movie.id), encoding="utf-8")
    info = folder / "physical.txt"
    info.write_text(f"Support: {movie.support}\nEmplacement origine: {movie.original_location}\nStatut: {movie.current_status}\n", encoding="utf-8")
    return folder

def export_all(movies: list[Movie]) -> int:
    count = 0
    for m in movies:
        export_movie(m)
        count += 1
    return count
