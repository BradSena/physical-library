from fastapi import FastAPI

app = FastAPI(
    title="Physical Library",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "name": "Physical Library",
        "version": "0.1.0",
        "status": "running"
    }
