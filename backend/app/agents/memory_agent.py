from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory


def memory_agent(state: PharmacyState) -> dict:
    """
    Memory Agent

    Responsibilities:
    - Fetch customer order history
    - Provide context to downstream agents
    - Emit judge-visible decision trace

    MUST return a DICT (LangGraph requirement)
    """

    db = SessionLocal()
    customer_id = state["customer"]["id"]

    try:
        history_rows = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer_id)
            .order_by(OrderHistory.created_at.desc())
            .limit(5)
            .all()
        )

        history = [
            {
                "medicine": row.medicine_name,
                "quantity": row.quantity,
                "date": row.created_at.isoformat()
            }
            for row in history_rows
        ]

        return {
            "meta": {
                "customer_history": history
            },
            "decision_trace": [
                {
                    "agent": "memory_agent",
                    "input": {"customer_id": customer_id},
                    "reasoning": f"Fetched {len(history)} previous orders",
                    "decision": "context_provided",
                    "output": history
                }
            ]
        }

    finally:
        db.close()
