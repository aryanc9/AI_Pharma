# backend/app/api/orders.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from backend.app.db.database import SessionLocal
from backend.app.services.order_service import create_order

router = APIRouter(prefix="/api/orders", tags=["Orders"])

class OrderItemRequest(BaseModel):
    medicine_id: int
    quantity: int
    dosage: Optional[str] = None

class OrderRequest(BaseModel):
    customer_id: int
    items: List[OrderItemRequest]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def place_order(order: OrderRequest, db: Session = Depends(get_db)):
    new_order = create_order(
        db,
        order.customer_id,
        [item.dict() for item in order.items]
    )
    return {"order_id": new_order.id, "status": "created"}
