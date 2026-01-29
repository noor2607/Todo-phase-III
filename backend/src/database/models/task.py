from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime


class TaskBase(SQLModel):
    """Base class for Task model with common fields"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(sa_column=Column(DateTime))
    user_id: str = Field(index=True)  # Foreign key reference to user, indexed for performance


class Task(TaskBase, table=True):
    """Task model for database storage"""
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow})


class TaskRead(TaskBase):
    """Schema for reading task data (includes ID and timestamps)"""
    id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Schema for updating task fields"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime))


class TaskCreate(TaskBase):
    """Schema for creating new tasks"""
    title: str = Field(min_length=1, max_length=200)
    # user_id will be set from the authenticated user, not from the request body