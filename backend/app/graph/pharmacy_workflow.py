from backend.app.graph.state import PharmacyState
from backend.app.graph.builder import build_pharmacy_graph
from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer


def run_workflow(customer_id: int, message: str) -> PharmacyState:
    """
    Entry point for the pharmacy agent workflow.

    RULES (CRITICAL):
    - conversation is INPUT ONLY
    - conversation is defined exactly ONCE here
    - no agent is allowed to overwrite conversation
    """

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise ValueError("Customer not found")

        # ✅ INITIAL STATE (single source of truth)
        initial_state: PharmacyState = {
            "conversation": {
                "message": message
            },
            "customer": {
                "id": customer.id,
                "name": customer.name
            },
            "extraction": {},
            "safety": {},
            "execution": {},
            "decision_trace": [],
            "meta": {}
        }

        # Build graph once
        graph = build_pharmacy_graph()

        # Execute graph
        final_state = graph.invoke(initial_state)

        return final_state

    except Exception as e:
        # Surface workflow errors cleanly to API
        raise RuntimeError(f"Workflow error: {str(e)}")

    finally:
        db.close()
