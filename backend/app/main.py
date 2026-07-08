from fastapi import FastAPI

from app.config import settings
from app.routes import auth, sync

app = FastAPI(title="DevLens API")
app.include_router(auth.router)
app.include_router(sync.router)


@app.get("/")
def root():
    return {"status": "DevLens API is running"}


@app.get("/health")
def health():
    return {"status": "ok", "database_configured": bool(settings.database_url)}
