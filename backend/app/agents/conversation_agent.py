import os
import re
from backend.app.graph.state import PharmacyState

USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"


def rule_based_extraction(message: str):
    """
    Production-safe deterministic extractor.
    """
    message_lower = message.lower()

    medicines = []
    quantity = 1
    dosage = None

    qty_match = re.search(r"\b(\d+)\b", message_lower)
    if qty_match:
        quantity = int(qty_match.group(1))

    dosage_match = re.search(r"(\d+\s?mg)", message_lower)
    if dosage_match:
        dosage = dosage_match.group(1)

    if "paracetamol" in message_lower:
        medicines.append({
            "name": "Paracetamol 500mg",
            "quantity": quantity,
            "dosage": dosage or "500mg"
        })

    intent = "order" if medicines else "unknown"

    return {
        "intent": intent,
        "medicines": medicines
    }


def conversation_agent(state: PharmacyState) -> PharmacyState:
    """
    Conversation Agent (Production Safe)
    """

    user_message = state["conversation"]["message"]

    # 🚨 Production-safe path
    extracted = rule_based_extraction(user_message)

    state["extraction"] = extracted

    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": user_message,
        "output": extracted,
        "decision": "rule_based_extraction"
    })

    return state
