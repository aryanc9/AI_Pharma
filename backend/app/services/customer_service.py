# backend/app/services/customer_service.py

from sqlalchemy.orm import Session
from app.db.models import Customer, CustomerHistory

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_history(db: Session, customer_id: int):
    return db.query(CustomerHistory).filter(
        CustomerHistory.customer_id == customer_id
    ).all()
