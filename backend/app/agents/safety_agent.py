from datetime import datetime
from sqlalchemy import func

from backend.app.graph.state import PharmacyState
from backend.app.db.database import SessionLocal
from backend.app.db.models import Medicine, Prescription
from backend.app.rules.safety_rules import MAX_QTY_PER_ORDER


def safety_agent(state: PharmacyState) -> PharmacyState:
    """
    Safety Agent (Rule-First, Deterministic)

    Responsibilities:
    - Validate medicine existence
    - Enforce stock limits
    - Enforce quantity limits
    - Enforce prescription requirements
    - Produce judge-visible reasoning
    """

    db = SessionLocal()

    violations = []
    reasoning_steps = []

    customer_id = state["customer"]["id"]
    medicines = state["extraction"].get("medicines", [])

    for item in medicines:
        name = item["name"].strip().lower()
        quantity = item["quantity"]

        # 1. Medicine existence (SQLite-safe, partial match)
        medicine = (
            db.query(Medicine)
            .filter(func.lower(Medicine.name).like(f"%{name}%"))
            .first()
        )

        if not medicine:
            violations.append(f"Medicine not found: {item['name']}")
            reasoning_steps.append(
                f"Medicine '{item['name']}' not found in inventory"
            )
            continue

        reasoning_steps.append(
            f"Found medicine '{medicine.name}' in database"
        )

        # 2. Quantity rule
        if quantity > MAX_QTY_PER_ORDER:
            violations.append(
                f"Quantity {quantity} exceeds allowed limit ({MAX_QTY_PER_ORDER})"
            )
            reasoning_steps.append(
                f"Requested quantity {quantity} exceeds max limit"
            )

        # 3. Stock check
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

        # 4. Prescription check
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
            reasoning_steps.append(
                f"No prescription required for {medicine.name}"
            )

    approved = len(violations) == 0

    # Final safety state
    state["safety"] = {
        "approved": approved,
        "reason": (
            "All safety checks passed"
            if approved
            else "Safety violations detected"
        ),
        "violations": violations
    }

    # Judge-visible trace (NO internal CoT leakage)
    state["decision_trace"].append({
        "agent": "safety_agent",
        "input": medicines,
        "reasoning": reasoning_steps,
        "decision": "approved" if approved else "blocked",
        "output": state["safety"]
    })

    db.close()
    return state
