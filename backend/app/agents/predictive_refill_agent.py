from datetime import datetime
from app.graph.state import PharmacyState
from app.db.database import SessionLocal
from app.db.models import OrderHistory


def predictive_refill_agent(state: PharmacyState) -> PharmacyState:
    assert isinstance(state, dict), f"STATE CORRUPTED: {type(state)}"

    db = SessionLocal()
    try:
        customer_id = state["customer"]["id"]

        history = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )

        alerts = []

        for record in history:
            days_since = (datetime.utcnow() - record.created_at).days
            if days_since >= 1:
                alerts.append({
                    "medicine": record.medicine_name,
                    "message": "Likely running low",
                })

        state["meta"]["refill_alerts"] = alerts

        state["decision_trace"].append({
            "agent": "predictive_refill_agent",
            "decision": "alerts_generated",
            "output": alerts,
        })

        return state

    finally:
        db.close()
