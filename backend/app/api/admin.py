from fastapi import APIRouter
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine, RefillAlert, OrderHistory
from backend.app.db.models import DecisionTrace

router = APIRouter(prefix="/admin")

@router.get("/decision-traces")
def list_decision_traces(limit: int = 50):
    db = SessionLocal()
    traces = (
        db.query(DecisionTrace)
        .order_by(DecisionTrace.created_at.desc())
        .limit(limit)
        .all()
    )
    db.close()
    return traces


@router.get("/medicines")
def list_medicines():
    db = SessionLocal()
    data = db.query(Medicine).all()
    db.close()
    return data

@router.get("/refill-alerts")
def list_refill_alerts():
    db = SessionLocal()
    data = db.query(RefillAlert).all()
    db.close()
    return data

@router.get("/orders")
def list_orders():
    db = SessionLocal()
    data = db.query(OrderHistory).all()
    db.close()
    return data
