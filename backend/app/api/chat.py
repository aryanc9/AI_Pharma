from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.db.database import SessionLocal
from app.db.models import Customer
from app.graph.pharmacy_workflow import run_workflow

router = APIRouter(prefix="/chat", tags=["chat"])


# 2️⃣ API RESPONSE SHAPING (Frontend-oriented)
# ChatResponse now supports:
# - approved: bool
# - error_type: VALIDATION, SAFETY, SYSTEM, or None
# - violations: list of specific errors
# - clarification_questions: list of missing info to ask user

class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    approved: bool
    reply: str
    order_id: Optional[int] = None
    error_type: Optional[str] = None  # VALIDATION, SAFETY, SYSTEM, or None if approved
    violations: Optional[List[str]] = None  # Detailed error information
    clarification_questions: Optional[List[str]] = None  # Missing info to ask user


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint with structured error responses.
    
    Decision types:
    - approved: Order placed
    - clarification_required: Ask user for more info, no violation
    - blocked: Safety violation, cannot proceed
    """
    db = SessionLocal()

    try:
        customer = db.query(Customer).filter(
            Customer.id == request.customer_id
        ).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        final_state = run_workflow(
            customer_id=customer.id,
            message=request.message
        )

        safety = final_state.get("safety", {})
        execution = final_state.get("execution", {})
        decision = safety.get("decision", "blocked")

        # 1C️⃣ CLARIFICATION INSTEAD OF HARD BLOCK
        # If clarification_required, ask the user
        if decision == "clarification_required":
            return ChatResponse(
                approved=False,
                reply="Please provide more information: " + "; ".join(safety.get("clarification_questions", [])),
                order_id=None,
                error_type=None,  # Not an error, just missing info
                violations=None,
                clarification_questions=safety.get("clarification_questions", [])
            )

        # If blocked, return structured error
        if not safety.get("approved"):
            return ChatResponse(
                approved=False,
                reply=safety.get("reason", "Request blocked by safety rules"),
                order_id=None,
                error_type=safety.get("error_type", "SAFETY"),
                violations=safety.get("violations", []),
                clarification_questions=None
            )

        # Success
        return ChatResponse(
            approved=True,
            reply="Order placed successfully",
            order_id=execution.get("order_id"),
            error_type=None,
            violations=None,
            clarification_questions=None
        )

    finally:
        db.close()
