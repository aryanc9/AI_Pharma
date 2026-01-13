from datetime import datetime, timedelta
from backend.app.db.database import SessionLocal
from backend.app.services.order_service import get_customer_history

def predictive_agent(customer_id: int):
    db = SessionLocal()
    history = get_customer_history(db, customer_id)

    predictions = []

    for record in history:
        last_purchase = record.purchase_date
        duration = record.prescribed_duration or 30

        expected_end = last_purchase + timedelta(days=duration)
        days_left = (expected_end - datetime.utcnow()).days

        if days_left <= 5:
            predictions.append({
                "customer_id": customer_id,
                "medicine": record.medicine_name,
                "days_left": days_left,
                "action": "proactive_refill"
            })

    return predictions
