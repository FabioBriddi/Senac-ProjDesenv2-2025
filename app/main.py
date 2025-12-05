from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from .db import init_db
from .routers import auth, sources, ingestions, reports

app = FastAPI(title="Music Insights Hub (SQLite)", version="0.1.0")


@app.on_event("startup")
def on_startup():
    init_db()


# APIs
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(sources.router, prefix="/sources", tags=["sources"])
app.include_router(ingestions.router, prefix="/ingestions", tags=["ingestions"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/health")
def health():
    return {"status": "ok"}


# Servir arquivos estáticos (HTML/JS/CSS) da pasta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")


# Rota raiz: devolve o index.html
@app.get("/", response_class=HTMLResponse)
def root():
    index_path = os.path.join("static", "index.html")
    with open(index_path, encoding="utf-8") as f:
        return f.read()
