from datetime import datetime, timedelta
import json

from app.db.database import SessionLocal, engine, Base
from app.db.models import (
    Customer, Medicine, Prescription, OrderHistory, 
    DecisionTrace, Order, OrderItem
)


def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create DB session
    db = SessionLocal()

    try:
        # ---------- Clear existing data (for re-seeding) ----------
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(DecisionTrace).delete()
        db.query(OrderHistory).delete()
        db.query(Prescription).delete()
        db.query(Customer).delete()
        db.query(Medicine).delete()
        db.commit()

        # ---------- CUSTOMERS ----------
        customers_data = [
            {"name": "John Smith", "email": "john@example.com", "phone": "555-0101", "language": "en", "is_new": False},
            {"name": "Sarah Johnson", "email": "sarah@example.com", "phone": "555-0102", "language": "en", "is_new": True},
            {"name": "Michael Chen", "email": "michael@example.com", "phone": "555-0103", "language": "zh", "is_new": False},
            {"name": "Emily Rodriguez", "email": "emily@example.com", "phone": "555-0104", "language": "es", "is_new": True},
            {"name": "David Wilson", "email": "david@example.com", "phone": "555-0105", "language": "en", "is_new": False},
            {"name": "Lisa Anderson", "email": "lisa@example.com", "phone": "555-0106", "language": "en", "is_new": True},
            {"name": "James Brown", "email": "james@example.com", "phone": "555-0107", "language": "en", "is_new": False},
            {"name": "Maria Garcia", "email": "maria@example.com", "phone": "555-0108", "language": "es", "is_new": True},
        ]
        
        customers = []
        for cust_data in customers_data:
            customer = Customer(
                name=cust_data["name"],
                email=cust_data["email"],
                phone=cust_data["phone"],
                preferred_language=cust_data["language"],
                is_new_user=cust_data["is_new"],
                created_at=datetime.utcnow() - timedelta(days=10 if not cust_data["is_new"] else 2)
            )
            customers.append(customer)
        
        db.add_all(customers)
        db.commit()

        # ---------- MEDICINES ----------
        medicines_data = [
            {"name": "Paracetamol 500mg", "stock": 100, "rx": False},
            {"name": "Ibuprofen 200mg", "stock": 150, "rx": False},
            {"name": "Amoxicillin 500mg", "stock": 45, "rx": True},
            {"name": "Metformin 500mg", "stock": 5, "rx": True},
            {"name": "Lisinopril 10mg", "stock": 0, "rx": True},
            {"name": "Omeprazole 20mg", "stock": 80, "rx": True},
            {"name": "Vitamin C 500mg", "stock": 200, "rx": False},
            {"name": "Aspirin 81mg", "stock": 120, "rx": False},
            {"name": "Cetirizine 10mg", "stock": 30, "rx": False},
            {"name": "Ciprofloxacin 500mg", "stock": 20, "rx": True},
        ]
        
        medicines = []
        for med_data in medicines_data:
            medicine = Medicine(
                name=med_data["name"],
                stock_quantity=med_data["stock"],
                prescription_required=med_data["rx"]
            )
            medicines.append(medicine)
        
        db.add_all(medicines)
        db.commit()

        # ---------- PRESCRIPTIONS ----------
        for customer in customers:
            # Assign random RX medicines to customers
            rx_medicines = [m for m in medicines if m.prescription_required]
            for med in rx_medicines[:2]:  # Each customer gets 2 prescriptions
                prescription = Prescription(
                    customer_id=customer.id,
                    medicine_id=med.id,
                    valid_until=datetime.utcnow() + timedelta(days=90)
                )
                db.add(prescription)
        
        db.commit()

        # ---------- ORDERS ----------
        order_count = 1
        for customer in customers:
            # Create 1-3 orders per customer
            for _ in range(1 if customer.is_new_user else 3):
                order = Order(
                    customer_id=customer.id,
                    created_at=datetime.utcnow() - timedelta(days=order_count)
                )
                db.add(order)
                db.flush()
                
                # Add order items
                for med in medicines[:3]:
                    order_item = OrderItem(
                        order_id=order.id,
                        medicine_id=med.id,
                        quantity=1 if med.prescription_required else 2,
                        dosage=med.name.split()[-1]
                    )
                    db.add(order_item)
                
                order_count += 1
        
        db.commit()

        # ---------- ORDER HISTORY ----------
        for customer in customers:
            orders = db.query(Order).filter(Order.customer_id == customer.id).all()
            for order in orders:
                for item in db.query(OrderItem).filter(OrderItem.order_id == order.id).all():
                    med = db.query(Medicine).filter(Medicine.id == item.medicine_id).first()
                    order_history = OrderHistory(
                        customer_id=customer.id,
                        medicine_name=med.name,
                        quantity=item.quantity,
                        created_at=order.created_at
                    )
                    db.add(order_history)
        
        db.commit()

        # ---------- DECISION TRACES ----------
        trace_count = 1
        for customer in customers:
            for i in range(2):  # 2 traces per customer
                trace = DecisionTrace(
                    request_id=f"req-{customer.id}-{i}",
                    agent_name=["safety_agent", "action_agent", "memory_agent", "conversation_agent"][i % 4],
                    input=json.dumps({
                        "customer_id": customer.id,
                        "message": f"Can I order medication? (trace {trace_count})"
                    }),
                    reasoning="Checked safety rules, verified prescription status, confirmed stock availability",
                    decision="APPROVED" if i % 2 == 0 else "PENDING_REVIEW",
                    output=json.dumps({
                        "approved": i % 2 == 0,
                        "reason": "Safety checks passed" if i % 2 == 0 else "Requires manual review",
                        "order_id": trace_count if i % 2 == 0 else None
                    }),
                    created_at=datetime.utcnow() - timedelta(hours=trace_count)
                )
                db.add(trace)
                trace_count += 1
        
        db.commit()

        print("✅ Database seeded successfully!")
        print(f"  📊 Customers: {db.query(Customer).count()}")
        print(f"  💊 Medicines: {db.query(Medicine).count()}")
        print(f"  📋 Prescriptions: {db.query(Prescription).count()}")
        print(f"  📦 Orders: {db.query(Order).count()}")
        print(f"  📝 Order History: {db.query(OrderHistory).count()}")
        print(f"  🔍 Decision Traces: {db.query(DecisionTrace).count()}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
