from datetime import datetime
from backend.app.db.database import SessionLocal
from backend.app.db.models import OrderHistory, RefillAlert, Customer

DEFAULT_DAYS_PER_UNIT = 1  # Explicit assumption


def estimate_days_remaining(quantity: int, days_since: int) -> int:
    total_days = quantity * DEFAULT_DAYS_PER_UNIT
    remaining = total_days - days_since
    return max(remaining, 0)


def urgency_from_days(days_remaining: int) -> str:
    if days_remaining <= 1:
        return "high"
    if days_remaining <= 3:
        return "medium"
    return "low"


def run_refill_engine():
    """
    Autonomous refill intelligence engine.
    Scans all customers and generates refill alerts.
    """

    db = SessionLocal()

    try:
        customers = db.query(Customer).all()

        for customer in customers:
            history = (
                db.query(OrderHistory)
                .filter(OrderHistory.customer_id == customer.id)
                .order_by(OrderHistory.created_at.desc())
                .all()
            )

            latest_by_medicine = {}
            for h in history:
                if h.medicine_name not in latest_by_medicine:
                    latest_by_medicine[h.medicine_name] = h

            for med_name, record in latest_by_medicine.items():
                days_since = (datetime.utcnow() - record.created_at).days
                days_remaining = estimate_days_remaining(record.quantity, days_since)

                if days_remaining <= 3:
                    urgency = urgency_from_days(days_remaining)

                    exists = (
                        db.query(RefillAlert)
                        .filter(
                            RefillAlert.customer_id == customer.id,
                            RefillAlert.medicine_name == med_name
                        )
                        .first()
                    )

                    if not exists:
                        db.add(
                            RefillAlert(
                                customer_id=customer.id,
                                medicine_name=med_name,
                                urgency=urgency,
                                days_remaining=days_remaining
                            )
                        )

                        print(
                            f"[REFILL ENGINE] "
                            f"customer={customer.id} "
                            f"medicine={med_name} "
                            f"days_remaining={days_remaining} "
                            f"urgency={urgency}"
                        )

        db.commit()

    finally:
        db.close()
