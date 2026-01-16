import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

# SQLite for local, Railway provides DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./pharmacy.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """
    Initialize database tables.
    IMPORTANT:
    - models import MUST be inside this function
    - prevents circular imports
    """
    from app.db import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
