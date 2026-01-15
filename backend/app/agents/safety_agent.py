from datetime import datetime
from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine, Prescription
from backend.app.rules.safety_rules import MAX_QTY_PER_ORDER


def safety_agent(state: PharmacyState) -> PharmacyState:
    # 🔒 HARD ASSERTION — non-negotiable
    assert isinstance(state, dict), f"STATE CORRUPTED: {type(state)}"

    db = SessionLocal()

    violations = []
    reasoning_steps = []

    customer_id = state["customer"]["id"]
    medicines = state.get("extraction", {}).get("medicines", [])
    print("SAFETY CHECK MEDICINES:", medicines)


    for item in medicines:
        name = item["name"]
        quantity = item["quantity"]

        # 1️⃣ Medicine existence (fuzzy match)
        medicine = (
            db.query(Medicine)
            .filter(Medicine.name.ilike(f"%{name}%"))
            .first()
        )

        if not medicine:
            violations.append(f"Medicine not found: {name}")
            reasoning_steps.append(
                f"Medicine '{name}' not found in inventory"
            )
            continue

        reasoning_steps.append(
            f"Found medicine '{medicine.name}' (prescription_required={medicine.prescription_required})"
        )

        # 2️⃣ Quantity rule
        if quantity > MAX_QTY_PER_ORDER:
            violations.append(
                f"Quantity {quantity} exceeds allowed limit ({MAX_QTY_PER_ORDER})"
            )
            reasoning_steps.append(
                f"Requested quantity {quantity} exceeds max limit"
            )

        # 3️⃣ Stock check
        if medicine.stock_quantity < quantity:
            violations.append(
                f"Insufficient stock for {medicine.name} "
                f"(available {medicine.stock_quantity})"
            )
            reasoning_steps.append(
                f"Stock insufficient for {medicine.name}"
            )
        else:
            reasoning_steps.append(
                f"Stock sufficient for {medicine.name}"
            )

        # 4️⃣ Prescription check — ONLY if required
        if medicine.prescription_required:
            prescription = (
                db.query(Prescription)
                .filter(
                    Prescription.customer_id == customer_id,
                    Prescription.medicine_id == medicine.id,
                    Prescription.valid_until >= datetime.utcnow()
                )
                .first()
            )

            if not prescription:
                violations.append(
                    f"Valid prescription required for {medicine.name}"
                )
                reasoning_steps.append(
                    f"No valid prescription found for {medicine.name}"
                )
            else:
                reasoning_steps.append(
                    f"Valid prescription found for {medicine.name}"
                )
        else:
            # ✅ OTC medicine — explicitly allowed
            reasoning_steps.append(
                f"{medicine.name} is OTC, no prescription required"
            )

    approved = len(violations) == 0

    state["safety"] = {
        "approved": approved,
        "reason": "All safety checks passed" if approved else "Safety violations detected",
        "violations": violations
    }

    state["decision_trace"].append({
        "agent": "safety_agent",
        "input": medicines,
        "reasoning": reasoning_steps,
        "decision": "approved" if approved else "blocked",
        "output": state["safety"]
    })

    db.close()
    return state
