from fastapi import FastAPI
from app.config import settings
from app.routes import auth

app = FastAPI(title="DevLens API")
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "DevLens API is running"}

@app.get("/health")
def health():
    return {"status": "ok", "database_configured": bool(settings.database_url)}
