from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine, OrderHistory
from backend.app.services.order_service import create_order
from datetime import datetime

print("🚀 ACTION AGENT LOADED")

def action_agent(state: PharmacyState) -> PharmacyState:
    """
    Action Agent (Execution + Proof Mode)

    This version PROVES:
    1. Safety approval status
    2. Medicines received from extraction
    3. Whether OrderHistory is actually written
    """

    print("\n🚀 ACTION AGENT EXECUTED")

    # ---------- PROOF 1: SAFETY STATE ----------
    print("🛡️ SAFETY STATE:", state.get("safety"))

    if not state.get("safety", {}).get("approved", False):
        print("⛔ EXECUTION BLOCKED BY SAFETY AGENT")
        return state

    print("✅ SAFETY APPROVED — CONTINUING EXECUTION")

    db = SessionLocal()

    medicines = state.get("extraction", {}).get("medicines", [])
    customer_id = state["customer"]["id"]

    # ---------- PROOF 2: MEDICINES RECEIVED ----------
    print("💊 MEDICINES RECEIVED:", medicines)

    if not medicines:
        print("❌ NO MEDICINES RECEIVED — NOTHING TO EXECUTE")
        return state

    execution_steps = []
    order_items = []

    try:
        for item in medicines:
            name = item["name"]
            quantity = item["quantity"]
            dosage = item.get("dosage", "")

            medicine = (
                db.query(Medicine)
                .filter(Medicine.name.ilike(f"%{name}%"))
                .with_for_update()
                .first()
            )

            if not medicine:
                raise ValueError(f"Medicine not found during execution: {name}")

            # Update inventory
            medicine.stock_quantity -= quantity

            order_items.append({
                "medicine_id": medicine.id,
                "quantity": quantity,
                "dosage": dosage
            })

            execution_steps.append(
                f"Resolved '{medicine.name}' (ID {medicine.id}), stock reduced by {quantity}"
            )

            # ---------- PROOF 3: ORDER HISTORY INSERT ----------
            print("📝 INSERTING ORDER HISTORY ROW FOR:", medicine.name)

            db.add(
                OrderHistory(
                    customer_id=customer_id,
                    medicine_name=medicine.name,
                    quantity=quantity,
                    created_at=datetime.utcnow()
                )
            )

        # Create order + order items
        order = create_order(db, customer_id, order_items)

        db.commit()

        # ---------- PROOF 4: VERIFY PERSISTENCE ----------
        count = db.query(OrderHistory).count()
        print("📊 ORDER HISTORY ROW COUNT (AFTER COMMIT):", count)

        state["execution"] = {
            "order_id": order.id,
            "actions": [
                "order_created",
                "inventory_updated",
                "order_history_saved"
            ]
        }

        state["decision_trace"].append({
            "agent": "action_agent",
            "input": medicines,
            "reasoning": execution_steps,
            "decision": "executed",
            "output": state["execution"]
        })

    except Exception as e:
        db.rollback()

        print("❌ EXECUTION FAILED:", str(e))

        state["execution"] = {
            "order_id": None,
            "actions": ["execution_failed"]
        }

        state["decision_trace"].append({
            "agent": "action_agent",
            "input": medicines,
            "reasoning": f"Execution failed: {str(e)}",
            "decision": "failed",
            "output": {"error": str(e)}
        })

    finally:
        db.close()

    return state
