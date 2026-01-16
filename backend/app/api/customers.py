from fastapi import APIRouter, Depends
from app.db.database import SessionLocal
from app.db.models import Customer
from app.security.admin_auth import admin_auth

"""
Customers Admin API

Purpose:
- View registered customers
- Used for auditing, debugging, and judge visibility
- Read-only (customers are created via seed or future onboarding)
"""

router = APIRouter(
    prefix="/admin/customers",
    tags=["admin"]
)


@router.get("/", dependencies=[Depends(admin_auth)])
def list_customers():
    """
    List all customers.

    Returns:
    - id
    - name
    - created_at (if present in model)
    """
    db = SessionLocal()
    try:
        customers = db.query(Customer).all()
        return customers
    finally:
        db.close()


@router.get("/{customer_id}", dependencies=[Depends(admin_auth)])
def get_customer(customer_id: int):
    """
    Get a single customer by ID.
    """
    db = SessionLocal()
    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            return {"error": "Customer not found"}

        return customer
    finally:
        db.close()
