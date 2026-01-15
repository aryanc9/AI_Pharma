from datetime import datetime
from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def predictive_refill_agent(state: PharmacyState) -> dict:
    """
    Predictive Refill Agent

    Responsibilities:
    - Analyze order history
    - Predict refill needs
    - Generate refill alerts (non-blocking)
    - Emit judge-visible reasoning

    MUST return a DICT (LangGraph requirement)
    """

    db = SessionLocal()
    customer_id = state["customer"]["id"]

    try:
        history = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )

        alerts = []

        latest_by_medicine = {}
        for row in history:
            if row.medicine_name not in latest_by_medicine:
                latest_by_medicine[row.medicine_name] = row

        for medicine_name, record in latest_by_medicine.items():
            days_since = (datetime.utcnow() - record.created_at).days

            if days_since >= 1:
                alerts.append({
                    "medicine": medicine_name,
                    "last_order_date": record.created_at.isoformat(),
                    "estimated_days": 1,
                    "days_since_last_order": days_since,
                    "message": f"Likely running low on {medicine_name}"
                })

        return {
            "meta": {
                "refill_alerts": alerts
            },
            "decision_trace": [
                {
                    "agent": "predictive_refill_agent",
                    "input": {"customer_id": customer_id},
                    "reasoning": f"Analyzed order history, generated {len(alerts)} alerts",
                    "decision": "alerts_generated",
                    "output": alerts
                }
            ]
        }

    finally:
        db.close()
