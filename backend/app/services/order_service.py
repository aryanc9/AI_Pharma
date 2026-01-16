# backend/app/services/order_service.py

from sqlalchemy.orm import Session
from app.db.models import Order, OrderItem

def create_order(db: Session, customer_id: int, items: list):
    order = Order(customer_id=customer_id)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        db.add(OrderItem(
            order_id=order.id,
            medicine_id=item["medicine_id"],
            quantity=item["quantity"],
            dosage=item.get("dosage", "")
        ))

    db.commit()
    return order
