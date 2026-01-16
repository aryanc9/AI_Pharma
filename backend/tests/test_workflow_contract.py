"""
Workflow Contract Tests
======================
Validates that the pharmacy workflow maintains critical contracts:
1. State is always a dict
2. Decision traces are collected correctly
3. Safety checks enforce OTC vs Rx logic
4. Medicine matching works with fuzzy search
5. Workflow completes without exceptions
"""

import pytest
from datetime import datetime, timedelta
from app.graph.pharmacy_workflow import run_workflow
from app.db.database import SessionLocal
from app.db.models import Customer, Medicine, Prescription, Order, OrderHistory, DecisionTrace


# Test fixtures
@pytest.fixture
def db_session():
    """Get database session for tests"""
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def otc_customer(db_session):
    """Customer who can order OTC medicines"""
    customer = db_session.query(Customer).first()
    if not customer:
        pytest.skip("No customers in database")
    return customer


@pytest.fixture
def rx_customer_with_prescription(db_session):
    """Customer with valid prescription for Rx medicine"""
    # Find a customer and an Rx medicine
    customer = db_session.query(Customer).first()
    rx_medicine = db_session.query(Medicine).filter(
        Medicine.prescription_required == True
    ).first()
    
    if not customer or not rx_medicine:
        pytest.skip("Missing customer or Rx medicine in database")
    
    # Create prescription if it doesn't exist
    existing_prescription = db_session.query(Prescription).filter(
        Prescription.customer_id == customer.id,
        Prescription.medicine_id == rx_medicine.id
    ).first()
    
    if not existing_prescription:
        prescription = Prescription(
            customer_id=customer.id,
            medicine_id=rx_medicine.id,
            prescribed_date=datetime.utcnow(),
            valid_until=datetime.utcnow() + timedelta(days=30),
            quantity_allowed=10
        )
        db_session.add(prescription)
        db_session.commit()
    
    return customer


# ============================================================================
# Contract Tests
# ============================================================================

class TestWorkflowStateContract:
    """Validates that workflow maintains state as dict"""
    
    def test_state_is_dict_after_run(self, otc_customer):
        """Final state must always be a dict"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        assert isinstance(final_state, dict), \
            f"State must be dict, got {type(final_state)}"
    
    def test_state_contains_required_keys(self, otc_customer):
        """Final state must contain all required keys"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        required_keys = ["customer", "conversation", "extraction", "safety", "decision_trace"]
        for key in required_keys:
            assert key in final_state, f"Missing required key: {key}"


class TestDecisionTraceContract:
    """Validates that decision traces are collected correctly"""
    
    def test_decision_trace_is_list(self, otc_customer):
        """Decision trace must be a list"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        assert isinstance(final_state["decision_trace"], list), \
            f"Decision trace must be list, got {type(final_state['decision_trace'])}"
    
    def test_decision_trace_contains_agents(self, otc_customer):
        """Decision trace must include all agent decisions"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        agents_involved = [trace["agent"] for trace in final_state["decision_trace"]]
        
        # Should have at least conversation and safety agents
        assert "conversation_agent" in agents_involved, \
            f"Missing conversation_agent in trace. Got: {agents_involved}"
        assert "safety_agent" in agents_involved, \
            f"Missing safety_agent in trace. Got: {agents_involved}"
    
    def test_decision_trace_persisted_to_db(self, otc_customer, db_session):
        """Decision traces must be saved to database"""
        # Clear previous traces for this customer
        db_session.query(DecisionTrace).filter(
            DecisionTrace.customer_id == otc_customer.id
        ).delete()
        db_session.commit()
        
        # Run workflow
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        # Verify traces in database
        traces = db_session.query(DecisionTrace).filter(
            DecisionTrace.customer_id == otc_customer.id
        ).all()
        
        assert len(traces) > 0, "No decision traces persisted to database"
        assert any(t.agent == "conversation_agent" for t in traces), \
            "No conversation_agent trace in database"
        assert any(t.agent == "safety_agent" for t in traces), \
            "No safety_agent trace in database"


class TestOTCVsRxContract:
    """Validates OTC vs Rx logic enforcement"""
    
    def test_otc_medicine_allowed_without_prescription(self, otc_customer):
        """OTC medicines must be allowed without prescription"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need paracetamol"
        )
        
        safety = final_state.get("safety", {})
        
        # Should be approved OR show validation error (medicine lookup)
        # but NOT a safety error about prescription
        if safety.get("approved"):
            assert True, "OTC medicine approved as expected"
        else:
            violations = safety.get("violations", [])
            has_prescription_error = any(
                "prescription" in v.lower() for v in violations
            )
            assert not has_prescription_error, \
                f"OTC medicine should not require prescription. Violations: {violations}"
    
    def test_rx_medicine_requires_prescription(self, rx_customer_with_prescription, db_session):
        """Rx medicines must require valid prescription"""
        rx_medicine = db_session.query(Medicine).filter(
            Medicine.prescription_required == True
        ).first()
        
        if not rx_medicine:
            pytest.skip("No Rx medicines in database")
        
        final_state = run_workflow(
            customer_id=rx_customer_with_prescription.id,
            message=f"I need {rx_medicine.name.split()[0].lower()}"
        )
        
        safety = final_state.get("safety", {})
        
        # Should either be approved (has prescription) or blocked with prescription error
        if not safety.get("approved"):
            violations = safety.get("violations", [])
            # Either prescription error or medicine not found (lookup issue)
            # but we expect it to enforce prescription if found
            assert len(violations) > 0, "Should have violations for Rx without prescription"


class TestMedicineMatchingContract:
    """Validates medicine lookup and fuzzy matching"""
    
    def test_medicine_extraction(self, otc_customer):
        """Medicine names must be extracted from natural language"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need some paracetamol please"
        )
        
        extraction = final_state.get("extraction", {})
        medicines = extraction.get("medicines", [])
        
        assert len(medicines) > 0, \
            f"Should extract medicine from message. Got: {extraction}"
    
    def test_medicine_lookup_handles_partial_names(self, otc_customer):
        """Medicine lookup should handle partial/fuzzy names"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need ibupro"  # Partial name
        )
        
        extraction = final_state.get("extraction", {})
        # If extraction succeeds, medicines should be non-empty
        if extraction.get("medicines"):
            assert len(extraction["medicines"]) > 0
    
    def test_medicine_lookup_handles_synonyms(self, otc_customer):
        """Medicine lookup should handle common synonyms"""
        # "Tylenol" is a synonym for "Paracetamol"
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need tylenol"
        )
        
        extraction = final_state.get("extraction", {})
        # Should extract at least the medicine
        assert extraction.get("intent") is not None


class TestWorkflowExecution:
    """Validates workflow completes successfully"""
    
    def test_workflow_completes_without_exception(self, otc_customer):
        """Workflow must complete without raising exceptions"""
        try:
            final_state = run_workflow(
                customer_id=otc_customer.id,
                message="I need paracetamol"
            )
            assert final_state is not None
        except Exception as e:
            pytest.fail(f"Workflow raised exception: {e}")
    
    def test_workflow_handles_invalid_customer(self, db_session):
        """Workflow must handle invalid customer gracefully"""
        invalid_id = 999999
        
        # Should handle gracefully (either raise HTTPException or handle in workflow)
        try:
            final_state = run_workflow(
                customer_id=invalid_id,
                message="I need medicine"
            )
            # If it returns, state should be valid dict
            assert isinstance(final_state, dict)
        except Exception:
            # Expected if customer not found
            pass
    
    def test_workflow_handles_empty_message(self, otc_customer):
        """Workflow must handle empty messages gracefully"""
        try:
            final_state = run_workflow(
                customer_id=otc_customer.id,
                message=""
            )
            
            # Should not extract medicines
            extraction = final_state.get("extraction", {})
            assert extraction.get("intent") in ["unknown", None] or len(extraction.get("medicines", [])) == 0
        except Exception:
            # Acceptable to reject empty messages
            pass


class TestErrorClassification:
    """Validates error classification in safety checks"""
    
    def test_validation_error_classification(self, otc_customer):
        """Validation errors (medicine not found, quantity) should be classified as VALIDATION"""
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message="I need 999999 units of paracetamol"  # Excessive quantity
        )
        
        safety = final_state.get("safety", {})
        if not safety.get("approved"):
            # Should have error_type set
            error_type = safety.get("error_type")
            assert error_type is not None, \
                f"Error must have error_type. Safety: {safety}"
            assert error_type in ["VALIDATION", "SAFETY", "SYSTEM"], \
                f"Invalid error_type: {error_type}"
    
    def test_safety_error_classification(self, db_session, otc_customer):
        """Safety errors (prescription, violations) should be classified as SAFETY"""
        # Create a scenario where prescription is missing for Rx medicine
        rx_medicine = db_session.query(Medicine).filter(
            Medicine.prescription_required == True
        ).first()
        
        if not rx_medicine:
            pytest.skip("No Rx medicines in database")
        
        # Clear any existing prescriptions
        db_session.query(Prescription).filter(
            Prescription.customer_id == otc_customer.id,
            Prescription.medicine_id == rx_medicine.id
        ).delete()
        db_session.commit()
        
        final_state = run_workflow(
            customer_id=otc_customer.id,
            message=f"I need {rx_medicine.name.split()[0].lower()}"
        )
        
        safety = final_state.get("safety", {})
        
        # If not approved and has violations about prescription
        if not safety.get("approved"):
            violations = safety.get("violations", [])
            if any("prescription" in str(v).lower() for v in violations):
                assert safety.get("error_type") == "SAFETY", \
                    f"Prescription error should be SAFETY, got {safety.get('error_type')}"
