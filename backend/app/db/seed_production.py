from app.db.database import SessionLocal, engine, Base
from app.db.models import Customer, Medicine

def seed_production_data():
    # 1️⃣ Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2️⃣ Seed default customer
        customer = db.query(Customer).first()
        if not customer:
            db.add(
                Customer(
                    name="Demo User",
                    phone="0000000000",
                    email="demo@aipharma.com",
                    is_new_user=False
                )
            )

        # 3️⃣ Seed medicines
        if db.query(Medicine).count() == 0:
            db.add_all([
                Medicine(
                    name="Paracetamol 500mg",
                    stock_quantity=100,
                    prescription_required=False
                ),
                Medicine(
                    name="Amoxicillin 500mg",
                    stock_quantity=50,
                    prescription_required=True
                )
            ])

        db.commit()
    finally:
        db.close()
