# backend/app/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    is_new_user = Column(Boolean, default=True)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    generic_name = Column(String)
    unit_type = Column(String)
    stock_quantity = Column(Integer)
    prescription_required = Column(Boolean)
    reorder_level = Column(Integer)
    price = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default="created")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    quantity = Column(Integer)
    dosage = Column(String)


class CustomerHistory(Base):
    __tablename__ = "customer_history"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    quantity = Column(Integer)
    dosage_frequency = Column(String)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())


class RefillAlert(Base):
    __tablename__ = "refill_alerts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    medicine_name = Column(String, nullable=False)
    urgency = Column(String, nullable=False)  # low | medium | high
    days_remaining = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderHistory(Base):

    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    medicine_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    medicine = relationship("Medicine")

class DecisionTrace(Base):
    __tablename__ = "decision_traces"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    agent = Column(String, nullable=False)
    input = Column(JSON, nullable=True)
    reasoning = Column(JSON, nullable=True)
    decision = Column(String, nullable=False)
    output = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
