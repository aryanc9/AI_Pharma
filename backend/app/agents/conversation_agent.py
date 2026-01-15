# backend/app/agents/conversation_agent.py

from backend.app.graph.state import PharmacyState
import re

def conversation_agent(state: PharmacyState) -> PharmacyState:
    assert isinstance(state, dict), f"STATE CORRUPTED: {type(state)}"

    message = state["conversation"]["message"].lower()

    medicines = []

    # Very simple deterministic extractor (production-safe)
    if "paracetamol" in message:
        medicines.append({
            "name": "Paracetamol",
            "quantity": 1,
            "dosage": "500mg"
        })

    state["extraction"] = {
        "intent": "order" if medicines else "unknown",
        "medicines": medicines
    }

    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": message,
        "reasoning": "Deterministic rule-based extraction (production)",
        "decision": "extracted",
        "output": state["extraction"]
    })

    return state
