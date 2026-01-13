# backend/app/api/medicines.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.database import SessionLocal
from backend.app.services.inventory_service import (
    get_all_medicines,
    get_medicine_by_id,
    update_stock
)

router = APIRouter(prefix="/api/medicines", tags=["Medicines"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_medicines(db: Session = Depends(get_db)):
    return get_all_medicines(db)

@router.get("/{medicine_id}")
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine = get_medicine_by_id(db, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.put("/{medicine_id}/stock")
def change_stock(
    medicine_id: int,
    quantity_change: int,
    db: Session = Depends(get_db)
):
    medicine = update_stock(db, medicine_id, quantity_change)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine
