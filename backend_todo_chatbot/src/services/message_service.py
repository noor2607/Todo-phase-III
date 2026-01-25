from sqlmodel import Session, select
from typing import List, Optional
from src.models import Message, MessageCreate


class MessageService:
    def create_message(self, db_session: Session, message_data: MessageCreate) -> Message:
        """Create a new message in a conversation."""
        message = Message.from_orm(message_data)
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    def get_messages_by_conversation(self, db_session: Session, conversation_id: int, user_id: int) -> List[Message]:
        """Get all messages for a conversation belonging to a user."""
        query = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at.asc())
        return db_session.exec(query).all()

    def get_message_by_id(self, db_session: Session, message_id: int, user_id: int) -> Optional[Message]:
        """Get a specific message by ID for a user."""
        query = select(Message).where(
            Message.id == message_id,
            Message.user_id == user_id
        )
        return db_session.exec(query).first()