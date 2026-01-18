from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    """Base class for User model with common fields"""
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User model for database storage"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    last_login_at: Optional[datetime] = Field(sa_column=Column(DateTime))


class UserRead(UserBase):
    """Schema for reading user data (includes ID and timestamps)"""
    id: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None


class UserCreate(UserBase):
    """Schema for creating new users"""
    password: str = Field(min_length=8, max_length=72)
    email: str = Field(max_length=255)
    username: str = Field(max_length=100)


class UserUpdate(SQLModel):
    """Schema for updating user fields"""
    email: Optional[str] = Field(default=None, max_length=255)
    username: Optional[str] = Field(default=None, max_length=100)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    """Schema for user login"""
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=72)


class UserRegister(UserCreate):
    """Schema for user registration"""
    pass