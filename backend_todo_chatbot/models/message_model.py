from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class MessageBase(SQLModel):
    role: str = Field(regex="^(user|assistant)$")  # Either "user" or "assistant"
    content: str = Field(min_length=1, max_length=5000)


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    conversation_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(MessageBase):
    id: int
    user_id: int
    conversation_id: int
    created_at: datetime


class MessageCreate(MessageBase):
    user_id: int
    conversation_id: int