from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer
from backend.app.graph.pharmacy_workflow import run_workflow

router = APIRouter(prefix="/chat", tags=["chat"])


# -----------------------------
# Request / Response Models
# -----------------------------
class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    approved: bool
    reply: str
    order_id: Optional[int] = None


# -----------------------------
# Chat Endpoint
# -----------------------------
@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    db = SessionLocal()

    try:
        # 1️⃣ Validate customer
        customer = (
            db.query(Customer)
            .filter(Customer.id == request.customer_id)
            .first()
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        # 2️⃣ Run agentic workflow (with crash visibility)
        try:
            final_state = run_workflow(
                customer_id=customer.id,
                message=request.message
            )
        except Exception as e:
            # 🔥 This guarantees visibility in Railway logs
            print("🔥 WORKFLOW CRASH:", repr(e))
            raise HTTPException(
                status_code=500,
                detail=f"Workflow error: {str(e)}"
            )

        # 3️⃣ Interpret result
        safety = final_state.get("safety", {})
        execution = final_state.get("execution", {})

        if not safety.get("approved", False):
            return ChatResponse(
                approved=False,
                reply="Request blocked by safety rules",
                order_id=None
            )

        return ChatResponse(
            approved=True,
            reply="Order placed successfully",
            order_id=execution.get("order_id")
        )

    finally:
        db.close()
