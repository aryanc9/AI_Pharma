# backend/app/services/inventory_service.py

from sqlalchemy.orm import Session
from backend.app.db.models import Medicine

def get_all_medicines(db: Session):
    return db.query(Medicine).all()

def get_medicine_by_id(db: Session, medicine_id: int):
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()

def update_stock(db: Session, medicine_id: int, quantity_change: int):
    medicine = get_medicine_by_id(db, medicine_id)
    if not medicine:
        return None
    medicine.stock_quantity += quantity_change
    db.commit()
    db.refresh(medicine)
    return medicine
