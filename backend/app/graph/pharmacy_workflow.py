from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

# Agents
from backend.app.agents.conversation_agent import conversation_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.agents.action_agent import action_agent

# Observability (optional)
from backend.app.observability.langfuse_client import langfuse


# -----------------------------
# State Definition
# -----------------------------
class PharmacyState(TypedDict):
    conversation: Dict[str, Any]
    customer: Dict[str, Any]
    extraction: Dict[str, Any]
    reasoning: Dict[str, Any]
    safety: Dict[str, Any]
    execution: Dict[str, Any]
    decision_trace: list
    meta: Dict[str, Any]


# -----------------------------
# Build LangGraph Workflow
# -----------------------------
def build_pharmacy_graph():
    graph = StateGraph(PharmacyState)

    graph.add_node("conversation_agent", conversation_agent)
    graph.add_node("safety_agent", safety_agent)
    graph.add_node("action_agent", action_agent)

    graph.set_entry_point("conversation_agent")
    graph.add_edge("conversation_agent", "safety_agent")

    graph.add_conditional_edges(
        "safety_agent",
        lambda state: "action_agent" if state["safety"].get("approved") else END
    )

    graph.add_edge("action_agent", END)

    return graph.compile()


# -----------------------------
# Run Workflow
# -----------------------------
def run_workflow():
    pharmacy_graph = build_pharmacy_graph()

    initial_state: PharmacyState = {
        "conversation": {"message": "I need paracetamol 500mg"},
        "customer": {"id": 1, "name": "Test User"},
        "extraction": {},
        "reasoning": {},
        "safety": {},
        "execution": {},
        "decision_trace": [],
        "meta": {}
    }

    final_state = pharmacy_graph.invoke(initial_state)

    # ---- SAFE OBSERVABILITY (NO CRASH) ----
    try:
        if hasattr(langfuse, "event"):
            langfuse.event(
                name="pharmacy_order_flow",
                metadata={
                    "customer_id": final_state["customer"]["id"],
                    "llm": "llama3.1:8b",
                    "decision_trace": final_state["decision_trace"]
                }
            )
    except Exception:
        pass  # Observability must NEVER block execution

    print("\nFINAL STATE:\n")
    print(final_state)

    print("\nDECISION TRACE (Judge-Visible CoT):\n")
    for step in final_state["decision_trace"]:
        print(step)


# -----------------------------
# CLI Entry
# -----------------------------
if __name__ == "__main__":
    run_workflow()
