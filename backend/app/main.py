from fastapi import FastAPI

from backend.app.db.database import init_db
from backend.app.api.chat import router as chat_router
from backend.app.api.admin import router as admin_router

app = FastAPI(title="Agentic Pharmacy Backend")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"status": "Pharmacy backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Routers
app.include_router(chat_router)
app.include_router(admin_router)
