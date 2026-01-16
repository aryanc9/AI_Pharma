from fastapi import APIRouter, Depends, HTTPException
from app.db.database import SessionLocal
from app.db.models import OrderHistory
from app.security.admin_auth import admin_auth

"""
Orders Admin API

Purpose:
- View historical orders placed by customers
- Used by admins, auditors, and judges
- Read-only (orders are created by agents)
"""

router = APIRouter(
    prefix="/admin/orders",
    tags=["admin"]
)


@router.get("/", dependencies=[Depends(admin_auth)])
def list_orders():
    """
    List all order history records.

    Admin-only endpoint.
    Returns:
    - customer_id
    - medicine_name
    - quantity
    - created_at
    """
    db = SessionLocal()
    try:
        orders = (
            db.query(OrderHistory)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )
        return orders
    finally:
        db.close()


@router.get("/{order_id}", dependencies=[Depends(admin_auth)])
def get_order_detail(order_id: int):
    """
    Get details of a specific order history record.
    
    Admin-only endpoint.
    Returns:
    - id
    - customer_id
    - medicine_name
    - quantity
    - created_at
    """
    db = SessionLocal()
    try:
        order = (
            db.query(OrderHistory)
            .filter(OrderHistory.id == order_id)
            .first()
        )
        
        if not order:
            raise HTTPException(
                status_code=404,
                detail=f"Order {order_id} not found"
            )
        
        return order
    finally:
        db.close()
