# backend/app/agents/conversation_agent.py

from app.graph.state import PharmacyState
import re

def conversation_agent(state: PharmacyState) -> PharmacyState:
    assert isinstance(state, dict), f"STATE CORRUPTED: {type(state)}"

    message = state["conversation"]["message"].lower()

    medicines = []

    # Medicine extraction rules (deterministic, production-safe)
    # Format: message_keyword → {name: db_name, dosage: default_dosage, otc: is_otc}
    medicine_rules = {
        "paracetamol": {"name": "Paracetamol 500mg", "dosage": "500mg", "otc": True},
        "acetaminophen": {"name": "Paracetamol 500mg", "dosage": "500mg", "otc": True},
        "tylenol": {"name": "Paracetamol 500mg", "dosage": "500mg", "otc": True},
        "ibuprofen": {"name": "Ibuprofen 200mg", "dosage": "200mg", "otc": True},
        "advil": {"name": "Ibuprofen 200mg", "dosage": "200mg", "otc": True},
        "motrin": {"name": "Ibuprofen 200mg", "dosage": "200mg", "otc": True},
        "amoxicillin": {"name": "Amoxicillin 500mg", "dosage": "500mg", "otc": False},
        "augmentin": {"name": "Amoxicillin 500mg", "dosage": "500mg", "otc": False},
        "metformin": {"name": "Metformin 500mg", "dosage": "500mg", "otc": False},
        "glucophage": {"name": "Metformin 500mg", "dosage": "500mg", "otc": False},
        "lisinopril": {"name": "Lisinopril 10mg", "dosage": "10mg", "otc": False},
        "zestril": {"name": "Lisinopril 10mg", "dosage": "10mg", "otc": False},
        "omeprazole": {"name": "Omeprazole 20mg", "dosage": "20mg", "otc": False},
        "prilosec": {"name": "Omeprazole 20mg", "dosage": "20mg", "otc": False},
        "vitamin c": {"name": "Vitamin C 500mg", "dosage": "500mg", "otc": True},
        "ascorbic acid": {"name": "Vitamin C 500mg", "dosage": "500mg", "otc": True},
        "aspirin": {"name": "Aspirin 81mg", "dosage": "81mg", "otc": True},
        "cetirizine": {"name": "Cetirizine 10mg", "dosage": "10mg", "otc": True},
        "zyrtec": {"name": "Cetirizine 10mg", "dosage": "10mg", "otc": True},
        "ciprofloxacin": {"name": "Ciprofloxacin 500mg", "dosage": "500mg", "otc": False},
        "cipro": {"name": "Ciprofloxacin 500mg", "dosage": "500mg", "otc": False},
    }

    # Extract quantity from message (patterns: "5 pills", "five units", "5x", "x5", "5 tablets")
    quantity_pattern = r'\b(\d+)\s*(?:pills?|units?|tablets?|caps?|x|dosages?|bottles?)'
    quantity_match = re.search(quantity_pattern, message, re.IGNORECASE)
    default_quantity = int(quantity_match.group(1)) if quantity_match else 1

    # Extract medicines from message
    for keyword, details in medicine_rules.items():
        if keyword in message:
            medicines.append({
                "name": details["name"],
                "quantity": default_quantity,
                "dosage": details["dosage"],
                "otc_hint": details["otc"]  # Help with safety checks
            })
            # Don't break - user might request multiple medicines

    state["extraction"] = {
        "intent": "order" if medicines else "unknown",
        "medicines": medicines
    }

    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": message,
        "reasoning": f"Extracted {len(medicines)} medicine(s) from message (quantity: {default_quantity})",
        "decision": "extracted" if medicines else "no_medicines_found",
        "output": state["extraction"]
    })

    return state
