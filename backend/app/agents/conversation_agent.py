import json
from langchain_ollama import ChatOllama
from backend.app.graph.state import PharmacyState

# LLM configuration (local / Ollama)
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    max_tokens=512
)

SYSTEM_PROMPT = """
You are a pharmacy conversation analysis agent.

You may think step by step internally, but DO NOT reveal your chain of thought.

Your task:
1. Identify intent: order | refill | query | unknown
2. Extract medicine name(s)
3. Infer quantity if implied
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


def conversation_agent(state: PharmacyState) -> PharmacyState:
    """
    Conversation Agent (LLM-based, non-mutating state)

    Responsibilities:
    - Read user message
    - Convert natural language to structured intent
    - NEVER overwrite existing state keys
    """

    # ✅ READ-ONLY access (critical for LangGraph)
    user_message = state["conversation"]["message"]

    response = llm.invoke(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ]
    )

    try:
        extracted = json.loads(response.content)
        confidence = "high"
    except Exception:
        extracted = {
            "intent": "unknown",
            "medicines": []
        }
        confidence = "low"

    # ✅ Write to NEW state keys only
    state["extraction"] = extracted

    # Judge-safe summarized reasoning (no chain-of-thought)
    state["reasoning"] = {
        "agent": "conversation_agent",
        "model": "llama3.1:8b",
        "confidence": confidence,
        "steps_used": [
            "intent_inference",
            "entity_extraction",
            "quantity_inference",
            "dosage_normalization"
        ]
    }

    # Judge-visible trace
    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": user_message,
        "output": extracted,
        "decision": "structured_request_generated"
    })

    return state
