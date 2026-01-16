from fastapi import APIRouter, Depends
from app.db.database import SessionLocal
from app.db.models import Medicine
from app.security.admin_auth import admin_auth

"""
Medicines Admin API

Purpose:
- View current inventory
- Acts as source of truth for stock and prescription rules
- Read-only (mutations handled by agents)
"""

router = APIRouter(
    prefix="/admin/medicines",
    tags=["admin"]
)


@router.get("/", dependencies=[Depends(admin_auth)])
def list_medicines():
    """
    List all medicines in inventory.

    Admin-only endpoint.
    """
    db = SessionLocal()
    try:
        medicines = db.query(Medicine).all()
        return medicines
    finally:
        db.close()
