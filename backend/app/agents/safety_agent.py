from datetime import datetime
from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine, Prescription
from backend.app.rules.safety_rules import MAX_QTY_PER_ORDER


def safety_agent(state: PharmacyState) -> PharmacyState:
    # 🚨 HARD ASSERTION
    assert isinstance(state, dict), f"STATE CORRUPTED in safety_agent: {type(state)}"

    db = SessionLocal()
    violations = []
    reasoning = []

    try:
        customer_id = state["customer"]["id"]
        medicines = state["extraction"].get("medicines", [])

        for item in medicines:
            name = item["name"]
            quantity = item["quantity"]

            medicine = (
                db.query(Medicine)
                .filter(Medicine.name.ilike(f"%{name}%"))
                .first()
            )

            if not medicine:
                violations.append(f"Medicine not found: {name}")
                reasoning.append(f"Medicine '{name}' not found")
                continue

            reasoning.append(f"Found medicine '{medicine.name}'")

            if quantity > MAX_QTY_PER_ORDER:
                violations.append("Quantity exceeds allowed limit")
                reasoning.append("Quantity limit violation")

            if medicine.stock_quantity < quantity:
                violations.append("Insufficient stock")
                reasoning.append("Stock insufficient")

            if medicine.prescription_required:
                prescription = (
                    db.query(Prescription)
                    .filter(
                        Prescription.customer_id == customer_id,
                        Prescription.medicine_id == medicine.id,
                        Prescription.valid_until >= datetime.utcnow(),
                    )
                    .first()
                )
                if not prescription:
                    violations.append("Prescription required")
                    reasoning.append("Missing prescription")

        approved = len(violations) == 0

        state["safety"] = {
            "approved": approved,
            "reason": "All safety checks passed" if approved else "Safety violations detected",
            "violations": violations,
        }

        state["decision_trace"].append({
            "agent": "safety_agent",
            "input": medicines,
            "reasoning": reasoning,
            "decision": "approved" if approved else "blocked",
            "output": state["safety"],
        })

        return state

    finally:
        db.close()
