from typing import Dict, Any, List
from datetime import datetime

from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def predictive_refill_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predictive Refill Agent

    - Analyzes customer order history
    - Estimates run-out dates
    - Generates refill alerts
    """

    db = SessionLocal()
    customer = state.get("customer", {})
    customer_id = customer.get("id")

    alerts: List[Dict[str, Any]] = []

    if customer_id:
        records = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .all()
        )

        latest_by_medicine = {}

        for r in records:
            if r.medicine_name not in latest_by_medicine:
                latest_by_medicine[r.medicine_name] = r

        today = datetime.utcnow()

        for medicine, record in latest_by_medicine.items():
            days_since = (today - record.created_at).days
            estimated_days = record.quantity

            if days_since >= int(estimated_days * 0.8):
                alerts.append({
                    "medicine": medicine,
                    "last_order_date": record.created_at.isoformat(),
                    "estimated_days": estimated_days,
                    "days_since_last_order": days_since,
                    "message": f"Likely running low on {medicine}"
                })

    state["meta"]["refill_alerts"] = alerts

    state["decision_trace"].append({
        "agent": "predictive_refill_agent",
        "input": {"customer_id": customer_id},
        "reasoning": f"Analyzed order history, generated {len(alerts)} alerts",
        "decision": "alerts_generated",
        "output": alerts
    })

    db.close()
    return state
