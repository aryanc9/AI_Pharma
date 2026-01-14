from datetime import datetime, timedelta

from backend.app.db.database import SessionLocal, engine, Base
from backend.app.db.models import Customer, Medicine, Prescription


def seed():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Create DB session
    db = SessionLocal()

    try:
        # ---------- Customers ----------
        if db.query(Customer).count() == 0:
            customer = Customer(name="Test User")
            db.add(customer)
            db.commit()
        else:
            customer = db.query(Customer).first()

        # ---------- Medicines ----------
        if db.query(Medicine).count() == 0:
            medicines = [
                Medicine(
                    name="Paracetamol 500mg",
                    stock_quantity=100,
                    prescription_required=False
                ),
                Medicine(
                    name="Amoxicillin 500mg",
                    stock_quantity=50,
                    prescription_required=True
                ),
            ]
            db.add_all(medicines)
            db.commit()

        medicines = db.query(Medicine).all()

        # ---------- Prescriptions ----------
        for med in medicines:
            if med.prescription_required:
                exists = (
                    db.query(Prescription)
                    .filter(
                        Prescription.customer_id == customer.id,
                        Prescription.medicine_id == med.id
                    )
                    .first()
                )

                if not exists:
                    db.add(
                        Prescription(
                            customer_id=customer.id,
                            medicine_id=med.id,
                            valid_until=datetime.utcnow() + timedelta(days=30)
                        )
                    )

        db.commit()

        print("✅ Database seeded successfully")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
