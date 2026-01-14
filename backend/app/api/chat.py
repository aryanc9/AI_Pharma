from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.graph.pharmacy_workflow import run_workflow
from backend.app.db.database import SessionLocal
from backend.app.db.models import Customer
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    customer_id: int
    message: str


class ChatResponse(BaseModel):
    approved: bool
    reply: str
    order_id: Optional[int] = None


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
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

        if not safety.get("approved"):
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
