from langgraph.graph import StateGraph, END

from backend.app.graph.state import PharmacyState
from backend.app.agents.memory_agent import memory_agent
from backend.app.agents.conversation_agent import conversation_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.agents.action_agent import action_agent
from backend.app.agents.predictive_refill_agent import predictive_refill_agent


def build_pharmacy_graph():
    """
    Build and compile the Agentic Pharmacy workflow graph.
    """

    graph = StateGraph(PharmacyState)

    # Nodes
    graph.add_node("memory", memory_agent)
    graph.add_node("conversation", conversation_agent)
    graph.add_node("safety", safety_agent)
    graph.add_node("action", action_agent)
    graph.add_node("predictive_refill", predictive_refill_agent)

    # Flow
    graph.set_entry_point("memory")
    graph.add_edge("memory", "conversation")
    graph.add_edge("conversation", "safety")

    graph.add_conditional_edges(
        "safety",
        lambda state: "action" if state["safety"].get("approved") else "predictive_refill"
    )

    graph.add_edge("action", "predictive_refill")
    graph.add_edge("predictive_refill", END)

    return graph.compile()
