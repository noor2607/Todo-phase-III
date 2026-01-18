from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize the database tables"""
    from database.models.task import Task  # Import here to avoid circular imports
    from database.models.user import User  # Import User model
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine, checkfirst=True)