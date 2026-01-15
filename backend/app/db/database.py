import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------
# Database path
# --------------------------------------------------
# Railway / Docker → use container filesystem
# Local → defaults to pharmacy.db in project root
DB_PATH = os.getenv("DB_PATH", "pharmacy.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

# --------------------------------------------------
# Engine
# --------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
    echo=False
)

# --------------------------------------------------
# Session
# --------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --------------------------------------------------
# Base
# --------------------------------------------------
Base = declarative_base()


# --------------------------------------------------
# Dependency (optional but recommended)
# --------------------------------------------------
def get_db():
    """
    FastAPI dependency for DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
