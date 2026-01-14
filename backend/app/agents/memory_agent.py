from typing import Dict, Any, List
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def memory_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Customer Memory Agent

    - Fetches recent order history
    - Adds context for other agents
    - Does NOT make decisions
    """

    db = SessionLocal()
    customer = state.get("customer", {})
    customer_id = customer.get("id")

    history: List[Dict[str, Any]] = []

    if customer_id:
        records = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .limit(5)
            .all()
        )

        for r in records:
            history.append({
                "medicine": r.medicine_name,
                "quantity": r.quantity,
                "date": r.created_at.isoformat()
            })

    state["meta"]["customer_history"] = history

    state["decision_trace"].append({
        "agent": "memory_agent",
        "input": {"customer_id": customer_id},
        "reasoning": f"Fetched {len(history)} previous orders",
        "decision": "context_provided",
        "output": history
    })

    db.close()
    return state
