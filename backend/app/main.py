from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.api.chat import router as chat_router
from app.api.admin import router as admin_router
from app.api.customers import router as customers_router
from app.api.medicines import router as medicines_router
from app.api.orders import router as orders_router
from app.api.decision_traces import router as decision_traces_router
from app.api.refill_alerts import router as refill_alerts_router

app = FastAPI(title="Agentic Pharmacy Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(customers_router)
app.include_router(medicines_router)
app.include_router(orders_router)
app.include_router(decision_traces_router)
app.include_router(refill_alerts_router)
