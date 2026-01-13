from fastapi import FastAPI
from backend.app.db.database import engine
from backend.app.db import models
from backend.app.api import medicines, customers, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic AI Pharmacy System")

app.include_router(medicines.router)
app.include_router(customers.router)
app.include_router(orders.router)

@app.get("/")
def health_check():
    return {"status": "Pharmacy backend running"}
