from backend.app.db.database import SessionLocal
from backend.app.services.inventory_service import get_all_medicines


def safety_agent(state):
    """
    Safety & Compliance Agent

    Responsibilities:
    - Enforce prescription requirements
    - Check stock availability
    - Decide APPROVE / REJECT deterministically
    - Explain WHY the decision was made (judge-visible)
    """

    db = SessionLocal()

    medicines_requested = state.get("extraction", {}).get("medicines", [])

    # Safety object always exists
    state["safety"] = {
        "approved": False,
        "reason": "Safety checks not executed"
    }

    # No medicines extracted
    if not medicines_requested:
        state["safety"] = {
            "approved": False,
            "reason": "No medicines requested"
        }

        state["decision_trace"].append({
            "agent": "safety_agent",
            "decision": "REJECTED",
            "checks": ["extraction_present"],
            "justification": "No medicines were extracted from user input"
        })
        return state

    inventory = get_all_medicines(db)
    inventory_map = {m.name.lower(): m for m in inventory}

    for item in medicines_requested:
        medicine_name = item["name"].lower()
        requested_qty = item["quantity"]

        # Medicine not found
        if medicine_name not in inventory_map:
            state["safety"] = {
                "approved": False,
                "reason": f"{item['name']} not found in inventory"
            }

            state["decision_trace"].append({
                "agent": "safety_agent",
                "decision": "REJECTED",
                "checks": ["inventory_lookup"],
                "justification": f"{item['name']} does not exist in inventory"
            })
            return state

        medicine = inventory_map[medicine_name]

        # Prescription required
        if medicine.prescription_required:
            state["safety"] = {
                "approved": False,
                "reason": f"{medicine.name} requires a valid prescription"
            }

            state["decision_trace"].append({
                "agent": "safety_agent",
                "decision": "REJECTED",
                "checks": ["prescription_rule"],
                "justification": {
                    "medicine": medicine.name,
                    "prescription_required": True
                }
            })
            return state

        # Insufficient stock
        if medicine.stock_quantity < requested_qty:
            state["safety"] = {
                "approved": False,
                "reason": f"Insufficient stock for {medicine.name}"
            }

            state["decision_trace"].append({
                "agent": "safety_agent",
                "decision": "REJECTED",
                "checks": ["inventory_quantity"],
                "justification": {
                    "medicine": medicine.name,
                    "requested": requested_qty,
                    "available": medicine.stock_quantity
                }
            })
            return state

    # All checks passed
    state["safety"] = {
        "approved": True,
        "reason": "All safety and compliance checks passed"
    }

    state["decision_trace"].append({
        "agent": "safety_agent",
        "decision": "APPROVED",
        "checks": [
            "inventory_lookup",
            "prescription_rule",
            "inventory_quantity"
        ],
        "justification": "Medicines are in stock and do not require a prescription"
    })

    return state
