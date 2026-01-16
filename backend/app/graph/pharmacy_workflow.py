import uuid
import json
from typing import Dict, Any

from langgraph.graph import StateGraph, END

from app.graph.state import PharmacyState
from app.db.database import SessionLocal
from app.db.models import DecisionTrace

from app.agents.memory_agent import memory_agent
from app.agents.conversation_agent import conversation_agent
from app.agents.safety_agent import safety_agent
from app.agents.action_agent import action_agent
from app.agents.predictive_refill_agent import predictive_refill_agent


# -------------------------
# Utilities
# -------------------------

def _safe_json(value):
    """
    Ensures SQLite-safe serialization.
    Prevents 'Error binding parameter - unsupported type'
    """
    if value is None:
        return None
    return json.dumps(value, default=str)


# -------------------------
# Graph Builder
# -------------------------

def build_pharmacy_graph():
    graph = StateGraph(PharmacyState)

    graph.add_node("memory_agent", memory_agent)
    graph.add_node("conversation_agent", conversation_agent)
    graph.add_node("safety_agent", safety_agent)
    graph.add_node("action_agent", action_agent)
    graph.add_node("predictive_refill_agent", predictive_refill_agent)

    graph.set_entry_point("memory_agent")

    graph.add_edge("memory_agent", "conversation_agent")
    graph.add_edge("conversation_agent", "safety_agent")
    graph.add_edge("safety_agent", "action_agent")
    graph.add_edge("action_agent", "predictive_refill_agent")
    graph.add_edge("predictive_refill_agent", END)

    return graph.compile()


# -------------------------
# Workflow Runner
# -------------------------

def run_workflow(customer_id: int, message: str) -> Dict[str, Any]:
    graph = build_pharmacy_graph()
    db = SessionLocal()

    request_id = str(uuid.uuid4())

    # ---- Initial State ----
    state: PharmacyState = {
        "conversation": {"message": message},
        "customer": {"id": customer_id},
        "extraction": {},
        "safety": {},
        "execution": {},
        "decision_trace": [],
        "meta": {},
    }

    # HARD ASSERT — NON NEGOTIABLE
    assert isinstance(state, dict), f"STATE CORRUPTED AT START: {type(state)}"

    try:
        final_state = graph.invoke(state)

        # HARD ASSERT — NON NEGOTIABLE
        assert isinstance(final_state, dict), f"STATE CORRUPTED AT END: {type(final_state)}"

        # -------------------------
        # Persist Decision Traces
        # -------------------------
        traces = final_state.get("decision_trace", [])

        for trace in traces:
            trace_row = DecisionTrace(
                request_id=request_id,
                agent_name=trace.get("agent"),
                input=_safe_json(trace.get("input")),
                reasoning=_safe_json(trace.get("reasoning")),
                decision=_safe_json(trace.get("decision")),
                output=_safe_json(trace.get("output")),
            )
            db.add(trace_row)

        db.commit()
        return final_state

    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Workflow error: {str(e)}")

    finally:
        db.close()
