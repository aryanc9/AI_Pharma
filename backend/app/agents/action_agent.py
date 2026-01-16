from app.graph.state import PharmacyState
from app.db.database import SessionLocal
from app.db.models import Medicine
from app.services.order_service import create_order


def action_agent(state: PharmacyState) -> PharmacyState:
    # 🚨 HARD ASSERTION
    assert isinstance(state, dict), f"STATE CORRUPTED in action_agent: {type(state)}"

    if not state.get("safety", {}).get("approved"):
        return state

    db = SessionLocal()
    try:
        customer_id = state["customer"]["id"]
        medicines = state["extraction"]["medicines"]

        order_items = []

        for item in medicines:
            medicine = (
                db.query(Medicine)
                .filter(Medicine.name.ilike(f"%{item['name']}%"))
                .with_for_update()
                .first()
            )

            medicine.stock_quantity -= item["quantity"]

            order_items.append({
                "medicine_id": medicine.id,
                "quantity": item["quantity"],
                "dosage": item.get("dosage", ""),
            })

        order = create_order(db, customer_id, order_items)

        state["execution"] = {
            "order_id": order.id,
            "actions": ["order_created", "inventory_updated"],
        }

        state["decision_trace"].append({
            "agent": "action_agent",
            "input": order_items,
            "decision": "executed",
            "output": state["execution"],
        })

        db.commit()
        return state

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
