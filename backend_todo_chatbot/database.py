from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from .models import *
import os
from typing import Generator


# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    """Get database session."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()