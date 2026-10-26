# project/starter/app/database.py
# Module 5 Project — Database setup
#
#Configure SQLAlchemy and implement the get_db dependency.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator
import os

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Load DATABASE_URL from environment (use python-dotenv or os.getenv)
BACKEND_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BACKEND_DIR / 'taskmanager.db'}"
)

# Create the engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass


# Implement get_db
def get_db() -> Generator[Session, None, None]:
    """Provides a DB session per request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
