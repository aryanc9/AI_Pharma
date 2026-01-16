import pytest
from app.graph.pharmacy_workflow import run_workflow
from app.db.database import SessionLocal
from app.db.models import Medicine, OrderHistory, Customer


@pytest.mark.integration
def test_pharmacy_workflow_happy_path():
    """
    WORKFLOW CONTRACT TEST

    Guarantees:
    - State remains dict throughout execution
    - Safety approves OTC medicine
    - Order is created
    - Inventory is reduced
    """

    db = SessionLocal()

    try:
        # --- Arrange -------------------------------------------------------
        customer = db.query(Customer).first()
        assert customer is not None, "Test requires at least one customer"

        medicine = (
            db.query(Medicine)
            .filter(Medicine.name.ilike("%Paracetamol%"))
            .first()
        )
        assert medicine is not None, "Paracetamol must exist for test"

        initial_stock = medicine.stock_quantity

        # --- Act -----------------------------------------------------------
        final_state = run_workflow(
            customer_id=customer.id,
            message="I need paracetamol 500mg"
        )

        # --- Assert: STATE CONTRACT ---------------------------------------
        assert isinstance(final_state, dict), "Final state must be a dict"
        assert "safety" in final_state
        assert "execution" in final_state

        # --- Assert: SAFETY -----------------------------------------------
        safety = final_state["safety"]
        assert safety["approved"] is True, "Safety must approve OTC order"
        assert safety["violations"] == []

        # --- Assert: EXECUTION --------------------------------------------
        execution = final_state["execution"]
        assert execution.get("order_id") is not None, "Order ID must exist"

        # --- Assert: DATABASE EFFECTS -------------------------------------
        db.refresh(medicine)
        assert medicine.stock_quantity == initial_stock - 1, (
            "Stock must decrement by ordered quantity"
        )

        order = (
            db.query(OrderHistory)
            .filter(OrderHistory.customer_id == customer.id)
            .order_by(OrderHistory.created_at.desc())
            .first()
        )

        assert order is not None, "OrderHistory record must exist"
        assert order.medicine_name.lower().startswith("paracetamol")

        # --- Assert: DECISION TRACE ---------------------------------------
        trace = final_state.get("decision_trace", [])
        agents = [step["agent"] for step in trace]

        assert agents == [
            "memory_agent",
            "conversation_agent",
            "safety_agent",
            "action_agent",
            "predictive_refill_agent",
        ], "Agent execution order must be stable"

    finally:
        db.close()
