from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
import httpx, os
from .db import init_db, get_session
from .models import Movie, CreateMovie, MoveMovie, DiscStatus
from .lookup import resolve_barcode, tmdb_search
from .export_kodi import export_movie, export_all

app = FastAPI(title="Physical Library", version="0.1.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><head><title>Physical Library</title><meta name='viewport' content='width=device-width,initial-scale=1'>
    <style>body{font-family:system-ui;margin:2rem;max-width:900px}input,button,select{font-size:1.1rem;padding:.5rem;margin:.2rem} .card{border:1px solid #ccc;border-radius:12px;padding:1rem;margin:.7rem 0}</style></head>
    <body><h1>📀 Physical Library</h1>
    <div class='card'><h2>Scan / saisie code-barres</h2><input id='barcode' autofocus placeholder='EAN / UPC'><button onclick='scan()'>Scanner</button><pre id='result'></pre></div>
    <div class='card'><h2>Ajouter manuel / validation</h2>
      <input id='title' placeholder='Titre'> <input id='year' placeholder='Année' size='4'><br>
      <input id='support' value='Blu-ray'> <input id='loc' placeholder='Emplacement origine ex: A3-027'><br>
      <input id='tmdb_id' placeholder='TMDb ID optionnel'><button onclick='addMovie()'>Ajouter</button>
    </div>
    <div class='card'><button onclick='exportAll()'>Exporter Kodi</button><button onclick='list()'>Liste</button><pre id='list'></pre></div>
    <script>
    async function scan(){let b=document.getElementById('barcode').value; let r=await fetch('/api/scan/'+b); let j=await r.json(); document.getElementById('result').textContent=JSON.stringify(j,null,2); if(j.best){title.value=j.best.title||''; year.value=j.best.year||''; support.value=j.best.support||'Blu-ray'; tmdb_id.value=j.best.tmdb_id||''}}
    async function addMovie(){let body={title:title.value, year:year.value?parseInt(year.value):null, barcode:barcode.value||null, support:support.value, original_location:loc.value, tmdb_id:tmdb_id.value?parseInt(tmdb_id.value):null}; let r=await fetch('/api/movies',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); alert(JSON.stringify(await r.json()));}
    async function list(){let r=await fetch('/api/movies'); document.getElementById('list').textContent=JSON.stringify(await r.json(),null,2)}
    async function exportAll(){let r=await fetch('/api/export/kodi',{method:'POST'}); alert(JSON.stringify(await r.json()))}
    </script></body></html>
    """

@app.get("/api/scan/{barcode}")
async def scan_barcode(barcode: str):
    return await resolve_barcode(barcode)

@app.get("/api/tmdb/search")
async def search_tmdb(q: str, year: int | None = None):
    return await tmdb_search(q, year)

@app.post("/api/movies", response_model=Movie)
def create_movie(payload: CreateMovie, session: Session = Depends(get_session)):
    movie = Movie(**payload.model_dump())
    session.add(movie)
    session.commit()
    session.refresh(movie)
    export_movie(movie)
    return movie

@app.get("/api/movies", response_model=list[Movie])
def list_movies(session: Session = Depends(get_session)):
    return session.exec(select(Movie).order_by(Movie.original_location)).all()

@app.get("/api/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404)
    return movie

@app.post("/api/movies/{movie_id}/move", response_model=Movie)
def move_movie(movie_id: int, payload: MoveMovie, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404)
    movie.current_status = payload.status
    movie.current_holder = payload.holder
    movie.expo_location = payload.expo_location
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie

@app.post("/api/export/kodi")
def export_kodi(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    count = export_all(movies)
    return {"exported": count}

@app.get("/api/kodi/play/{movie_id}")
async def kodi_play(movie_id: int, session: Session = Depends(get_session)):
    movie = session.get(Movie, movie_id)
    if not movie:
        raise HTTPException(404)
    webhook = os.getenv("HA_WEBHOOK_URL")
    if webhook:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(webhook, json={"event":"physical_disc_requested","movie_id": movie.id, "title": movie.title, "support": movie.support, "original_location": movie.original_location, "status": movie.current_status})
        except Exception:
            pass
    return {"message": f"Insérer le disque : {movie.title}", "support": movie.support, "original_location": movie.original_location, "status": movie.current_status, "holder": movie.current_holder, "expo_location": movie.expo_location}
