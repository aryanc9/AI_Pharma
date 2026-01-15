import json
from langchain_ollama import ChatOllama
from backend.app.graph.state import PharmacyState


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    max_tokens=512,
)

SYSTEM_PROMPT = """
You are a pharmacy conversation analysis agent.

Return ONLY valid JSON.
Do NOT explain anything.

Schema:
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
    # 🚨 HARD ASSERTION
    assert isinstance(state, dict), f"STATE CORRUPTED in conversation_agent: {type(state)}"

    user_message = state["conversation"]["message"]

    response = llm.invoke([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ])

    try:
        extracted = json.loads(response.content)
        confidence = "high"
    except Exception:
        extracted = {"intent": "unknown", "medicines": []}
        confidence = "low"

    state["extraction"] = extracted

    state["decision_trace"].append({
        "agent": "conversation_agent",
        "input": user_message,
        "output": extracted,
        "confidence": confidence,
    })

    return state
