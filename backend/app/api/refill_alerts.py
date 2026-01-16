from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.models import Medicine, Order
from app.security.admin_auth import admin_auth

"""
Refill Alerts Admin API

Purpose:
- Identify medicines that need refilling (low stock)
- Identify customers with refill alerts (auto-refill due)
- Used by admins and operations team
"""

router = APIRouter(
    prefix="/admin/refill-alerts",
    tags=["admin"]
)

# Stock levels for alerting
LOW_STOCK_THRESHOLD = 20  # Alert if below this
CRITICAL_STOCK_THRESHOLD = 5  # Critical if below this


@router.get("/", dependencies=[Depends(admin_auth)])
def list_refill_alerts():
    """
    List all medicines that need refilling.
    
    Admin-only endpoint.
    Returns medicines with:
    - status: "CRITICAL" (0-5 units) or "LOW" (5-20 units)
    - current_stock
    - reorder_point
    - suggested_order_qty
    """
    db = SessionLocal()
    try:
        # Find all medicines below stock threshold
        medicines = (
            db.query(Medicine)
            .filter(Medicine.stock_quantity <= LOW_STOCK_THRESHOLD)
            .order_by(Medicine.stock_quantity.asc())
            .all()
        )
        
        alerts = []
        for medicine in medicines:
            status = "CRITICAL" if medicine.stock_quantity <= CRITICAL_STOCK_THRESHOLD else "LOW"
            
            alerts.append({
                "id": medicine.id,
                "name": medicine.name,
                "current_stock": medicine.stock_quantity,
                "status": status,
                "reorder_point": LOW_STOCK_THRESHOLD,
                "suggested_order_qty": 100,  # Standard reorder quantity
                "prescription_required": medicine.prescription_required,
                "alert_priority": "CRITICAL" if status == "CRITICAL" else "HIGH"
            })
        
        return alerts
    finally:
        db.close()


@router.get("/customer/{customer_id}", dependencies=[Depends(admin_auth)])
def get_customer_refill_alerts(customer_id: int):
    """
    Get refill alerts for a specific customer.
    
    Admin-only endpoint.
    Returns list of medicines eligible for auto-refill:
    - Last order date
    - Days since last order
    - Refill eligibility (e.g., 30 days between refills)
    - Suggested next order date
    """
    db = SessionLocal()
    try:
        # Find recent orders for this customer
        orders = (
            db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .limit(20)
            .all()
        )
        
        alerts = []
        now = datetime.utcnow()
        refill_interval_days = 30  # Standard refill interval
        
        for order in orders:
            days_since = (now - order.created_at).days
            next_eligible_date = order.created_at + timedelta(days=refill_interval_days)
            is_eligible = now >= next_eligible_date
            
            alerts.append({
                "order_id": order.id,
                "medicine_id": order.medicine_id,
                "last_order_date": order.created_at.isoformat(),
                "days_since_order": days_since,
                "refill_eligible": is_eligible,
                "next_eligible_date": next_eligible_date.isoformat(),
                "refill_priority": "READY" if is_eligible else "PENDING"
            })
        
        return alerts
    finally:
        db.close()
