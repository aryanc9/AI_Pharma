# backend/app/db/seed_data.py

from .database import SessionLocal, engine, Base
from .models import Customer, Medicine

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Medicine).count() == 0:
        db.add_all([
            Medicine(
                name="Paracetamol 500mg",
                generic_name="Paracetamol",
                unit_type="tablet",
                stock_quantity=200,
                prescription_required=False,
                reorder_level=50,
                price=20
            ),
            Medicine(
                name="Amlodipine 5mg",
                generic_name="Amlodipine",
                unit_type="tablet",
                stock_quantity=120,
                prescription_required=True,
                reorder_level=30,
                price=50
            )
        ])

    if db.query(Customer).count() == 0:
        db.add(
            Customer(
                name="John Doe",
                phone="9999999999",
                email="john@example.com",
                is_new_user=False
            )
        )

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
