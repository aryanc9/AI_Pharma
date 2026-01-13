# backend/app/api/customers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal
from backend.app.services.customer_service import (
    get_customer,
    get_customer_history
)

router = APIRouter(prefix="/api/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{customer_id}")
def fetch_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/{customer_id}/history")
def fetch_customer_history(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_history(db, customer_id)
