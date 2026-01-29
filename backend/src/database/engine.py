from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Generator, AsyncGenerator
import os
from contextlib import contextmanager
from contextlib import asynccontextmanager

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Determine database type for proper connect_args
is_sqlite = DATABASE_URL.startswith("sqlite:///")
is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")

# Fix the async database URL format
if is_sqlite:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite:///", 1)
elif DATABASE_URL.startswith("postgresql://"):
    # Convert PostgreSQL to asyncpg driver
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    # Convert postgres:// to asyncpg driver
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# SQLite needs check_same_thread, PostgreSQL doesn't
sqlite_connect_args = {"check_same_thread": False} if is_sqlite else {}
async_sqlite_connect_args = {"check_same_thread": False} if is_sqlite else {}

# Create the engines
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=sqlite_connect_args
)
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    connect_args=async_sqlite_connect_args
)


def get_session() -> Generator[Session, None, None]:
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session for dependency injection"""
    async with AsyncSession(async_engine) as session:
        yield session


def init_db():
    """Initialize the database tables"""
    from database.models.task import Task  # Import here to avoid circular imports
    from database.models.user import User  # Import User model
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine, checkfirst=True)


async def init_db_async():
    """Initialize the database tables asynchronously"""
    from database.models.task import Task  # Import here to avoid circular imports
    from database.models.user import User  # Import User model
    from sqlmodel import SQLModel

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
