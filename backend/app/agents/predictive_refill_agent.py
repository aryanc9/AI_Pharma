from datetime import datetime
from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def predictive_refill_agent(state: PharmacyState) -> PharmacyState:
    # 🚨 HARD ASSERTION
    assert isinstance(state, dict), f"STATE CORRUPTED in predictive_refill_agent: {type(state)}"

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
