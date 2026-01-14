from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from backend.app.graph.state import PharmacyState
from backend.app.agents.memory_agent import memory_agent
from backend.app.agents.conversation_agent import conversation_agent
from backend.app.agents.safety_agent import safety_agent
from backend.app.agents.action_agent import action_agent
from backend.app.agents.predictive_refill_agent import predictive_refill_agent

from backend.app.db.database import SessionLocal
from backend.app.db.models import DecisionTrace
from backend.app.db.models import Customer
from backend.app.graph.builder import build_pharmacy_graph


# -------------------------------------------------------------------
# Persist decision traces (audit-grade observability)
# -------------------------------------------------------------------

def persist_decision_traces(state: PharmacyState):
    db = SessionLocal()
    try:
        for trace in state.get("decision_trace", []):
            db.add(
                DecisionTrace(
                    customer_id=state["customer"]["id"],
                    agent=trace.get("agent"),
                    input=trace.get("input"),
                    reasoning=trace.get("reasoning"),
                    decision=trace.get("decision"),
                    output=trace.get("output"),
                )
            )
        db.commit()
    finally:
        db.close()


# -------------------------------------------------------------------
# Graph Builder
# -------------------------------------------------------------------

def build_pharmacy_graph():
    graph = StateGraph(PharmacyState)

    # Nodes (agents)
    graph.add_node("memory", memory_agent)
    graph.add_node("conversation", conversation_agent)
    graph.add_node("safety", safety_agent)
    graph.add_node("action", action_agent)
    graph.add_node("predictive_refill", predictive_refill_agent)

    # Flow
    graph.set_entry_point("memory")
    graph.add_edge("memory", "conversation")
    graph.add_edge("conversation", "safety")

    # Safety gate
    graph.add_conditional_edges(
        "safety",
        lambda state: "action" if state["safety"]["approved"] else "predictive_refill",
        {
            "action": "action",
            "predictive_refill": "predictive_refill",
        },
    )

    graph.add_edge("action", "predictive_refill")
    graph.add_edge("predictive_refill", END)

    return graph.compile()


# -------------------------------------------------------------------
# CLI / Script Runner (optional, but useful)
# -------------------------------------------------------------------

def run_workflow(customer_id: int, message: str) -> PharmacyState:
    """
    Public entrypoint for the Agentic Pharmacy Workflow.
    Used by API, CLI, and tests.
    """

    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise ValueError("Customer not found")

        initial_state: PharmacyState = {
            "conversation": {"message": message},
            "customer": {"id": customer.id, "name": customer.name},
            "extraction": {},
            "safety": {},
            "execution": {},
            "decision_trace": [],
            "meta": {}
        }

        pharmacy_graph = build_pharmacy_graph()
        final_state = pharmacy_graph.invoke(initial_state)

        return final_state

    finally:
        db.close()


# -------------------------------------------------------------------
# Allow `python -m backend.app.graph.pharmacy_workflow`
# -------------------------------------------------------------------

if __name__ == "__main__":
    run_workflow()
