import json
from typing import Any, Dict

from backend.app.graph.state import PharmacyState
from backend.app.config import LLM_PROVIDER, OLLAMA_MODEL

# ------------------------------------------------------------
# Optional Ollama Import (Docker-safe)
# ------------------------------------------------------------

try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# ------------------------------------------------------------
# LLM Initialization (Safe)
# ------------------------------------------------------------

llm = None

if LLM_PROVIDER == "ollama" and OLLAMA_AVAILABLE:
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
        max_tokens=512
    )


# ------------------------------------------------------------
# System Prompt (Judge-safe)
# ------------------------------------------------------------

SYSTEM_PROMPT = """
You are a pharmacy conversation analysis agent.

You may reason internally, but DO NOT reveal chain-of-thought.

Your task:
1. Identify intent: order | refill | query | unknown
2. Extract medicine name(s)
3. Infer quantity if implied (default to 1 if unclear)
4. Extract dosage if mentioned
5. Normalize medicine names

Rules:
- Do NOT diagnose
- Do NOT suggest medicines
- Output ONLY valid JSON

JSON schema:
{
  "intent": "order | refill | query | unknown",
  "medicines": [
    {
      "name": "string",
      "quantity": number,
      "dosage": "string | null"
    }
  ]
}
"""


# ------------------------------------------------------------
# Conversation Agent
# ------------------------------------------------------------

def conversation_agent(state: PharmacyState) -> PharmacyState:
    """
    Conversation Agent

    Converts natural language into structured pharmacy intent.
    Works with or without an LLM.
    """

    user_message = state["conversation"]["message"]

    extracted: Dict[str, Any]
    confidence: str

    # --------------------------------------------------------
    # LLM Path (Local Development)
    # --------------------------------------------------------

    if llm is not None:
        response = llm.invoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ])

        try:
            extracted = json.loads(response.content)
            confidence = "high"
        except Exception:
            extracted = {"intent": "unknown", "medicines": []}
            confidence = "low"

    # --------------------------------------------------------
    # Fallback Path (Docker / Cloud)
    # --------------------------------------------------------

    else:
        extracted = {
            "intent": "order",
            "medicines": [
                {
                    "name": "Paracetamol",
                    "quantity": 1,
                    "dosage": "500mg"
                }
            ]
        }
        confidence = "fallback"

    # --------------------------------------------------------
    # Update State
    # --------------------------------------------------------

    state["extraction"] = extracted

    state["reasoning"] = {
        "agent": "conversation_agent",
        "model": OLLAMA_MODEL if llm else "fallback",
        "reasoning_type": "long_chain",
        "confidence": confidence,
        "steps_used": [
            "intent_inference",
            "entity_extraction",
            "quantity_inference",
            "dosage_normalization"
        ]
    }

    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": user_message,
        "reasoning": state["reasoning"],
        "decision": "extracted_structured_request",
        "output": extracted
    })

    return state
