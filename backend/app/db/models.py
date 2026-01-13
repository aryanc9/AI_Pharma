# backend/app/db/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

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
    customer_id = Column(Integer, ForeignKey("customers.id"))
    medicine_id = Column(Integer, ForeignKey("medicines.id"))
    days_remaining = Column(Integer)
    alert_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
