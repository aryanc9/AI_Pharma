from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.sql import func

from backend.app.db.base import Base


# -------------------------
# CUSTOMER
# -------------------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)

    is_new_user = Column(Boolean, default=True)
    preferred_language = Column(String, default="en")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# -------------------------
# MEDICINE
# -------------------------
class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    stock_quantity = Column(Integer, default=0)
    prescription_required = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# -------------------------
# PRESCRIPTION
# -------------------------
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
        nullable=False
    )

    valid_until = Column(DateTime, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# -------------------------
# ORDER HISTORY
# -------------------------
class OrderHistory(Base):
    __tablename__ = "order_history"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    medicine_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# -------------------------
# DECISION TRACE
# -------------------------
class DecisionTrace(Base):
    __tablename__ = "decision_traces"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(String, index=True)
    agent_name = Column(String)

    input = Column(Text)
    reasoning = Column(Text)
    decision = Column(String)
    output = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

# -------------------------
# ORDER
# -------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# -------------------------
# ORDER ITEM
# -------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)
    dosage = Column(String, nullable=True)
