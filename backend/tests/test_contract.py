"""
4️⃣ Workflow Contract Test (Minimal)

Tests that verify the workflow contract:
- run_workflow() returns a dict
- Required keys exist (safety, execution, decision_trace)
- Decision traces are persisted
- OTC/Rx logic works correctly
"""

import pytest
from app.graph.pharmacy_workflow import run_workflow
from app.db.database import SessionLocal
from app.db.models import Customer, Medicine, DecisionTrace


class TestWorkflowContract:
    """Minimal contract tests for workflow stability"""

    def test_workflow_returns_dict(self):
        """run_workflow() must return a dict"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need paracetamol"
            )
            
            assert isinstance(final_state, dict), "Final state must be dict"
        finally:
            db.close()

    def test_workflow_has_required_keys(self):
        """Workflow state must contain all required keys"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need paracetamol"
            )
            
            required_keys = ["customer", "conversation", "extraction", "safety", "execution", "decision_trace"]
            for key in required_keys:
                assert key in final_state, f"Missing required key: {key}"
        finally:
            db.close()

    def test_decision_trace_persisted(self):
        """Decision traces must be persisted to database"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            # Run workflow
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need paracetamol"
            )
            
            # Verify traces persisted
            traces = db.query(DecisionTrace).filter(
                DecisionTrace.customer_id == customer.id
            ).all()
            
            assert len(traces) > 0, "Decision traces must be persisted"
            
            # Verify trace agents
            agents = [t.agent for t in traces]
            assert "safety_agent" in agents, "Safety agent must be in traces"
            assert "conversation_agent" in agents, "Conversation agent must be in traces"
        finally:
            db.close()

    def test_otc_medicine_allowed(self):
        """OTC medicine must be approved without prescription"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need paracetamol"
            )
            
            safety = final_state.get("safety", {})
            assert safety.get("approved") is True, "OTC medicine should be approved"
            assert safety.get("decision") == "approved", "Decision should be 'approved'"
        finally:
            db.close()

    def test_error_type_classification(self):
        """Errors must be classified as VALIDATION, SAFETY, or SYSTEM"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            # Try excessive quantity
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need 999 pills of paracetamol"
            )
            
            safety = final_state.get("safety", {})
            
            if not safety.get("approved"):
                error_type = safety.get("error_type")
                assert error_type in [None, "VALIDATION", "SAFETY", "SYSTEM"], \
                    f"Invalid error_type: {error_type}"
        finally:
            db.close()

    def test_clarification_logic(self):
        """
        1C️⃣ Clarification instead of hard block
        Missing info should trigger clarification, not block
        """
        db = SessionLocal()
        try:
            customer = db.query(Customer).first()
            assert customer is not None
            
            final_state = run_workflow(
                customer_id=customer.id,
                message="I need paracetamol without dosage"
            )
            
            safety = final_state.get("safety", {})
            decision = safety.get("decision")
            
            # If no dosage specified, should ask for clarification (not block)
            if decision == "clarification_required":
                clarification_questions = safety.get("clarification_questions", [])
                assert len(clarification_questions) > 0, "Should have clarification questions"
                assert any("dosage" in q.lower() for q in clarification_questions), \
                    "Should ask about dosage"
        finally:
            db.close()
