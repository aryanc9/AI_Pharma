from typing import Dict, Any

from langgraph.graph import StateGraph, END

from backend.app.graph.state import PharmacyState

from backend.app.agents.memory_agent import memory_agent
from backend.app.agents.conversation_agent import conversation_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.agents.action_agent import action_agent
from backend.app.agents.predictive_refill_agent import predictive_refill_agent


def build_pharmacy_graph():
    """
    Builds the LangGraph workflow for the pharmacy system.

    IMPORTANT RULE:
    - Each agent must MUTATE and RETURN the SAME state dict
    - No agent may replace the state object
    """

    graph = StateGraph(PharmacyState)

    # Register agents as pure state transformers
    graph.add_node("memory_agent", memory_agent)
    graph.add_node("conversation_agent", conversation_agent)
    graph.add_node("safety_agent", safety_agent)
    graph.add_node("action_agent", action_agent)
    graph.add_node("predictive_refill_agent", predictive_refill_agent)

    # Define execution order
    graph.set_entry_point("memory_agent")

    graph.add_edge("memory_agent", "conversation_agent")
    graph.add_edge("conversation_agent", "safety_agent")
    graph.add_edge("safety_agent", "action_agent")
    graph.add_edge("action_agent", "predictive_refill_agent")
    graph.add_edge("predictive_refill_agent", END)

    return graph.compile()


def run_workflow(customer_id: int, message: str) -> Dict[str, Any]:
    """
    Executes the pharmacy workflow for a single chat request.
    """

    graph = build_pharmacy_graph()

    # INITIAL STATE — must be a DICT, not a set
    initial_state: PharmacyState = {
        "conversation": {
            "message": message
        },
        "customer": {
            "id": customer_id
        },
        "extraction": {},
        "safety": {},
        "execution": {},
        "decision_trace": [],
        "meta": {}
    }

    try:
        final_state = graph.invoke(initial_state)
        return final_state

    except Exception as e:
        # Always raise a clean error for API layer
        raise RuntimeError(f"Workflow error: {str(e)}")
