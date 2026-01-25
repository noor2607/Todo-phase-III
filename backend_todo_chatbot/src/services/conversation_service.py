from sqlmodel import Session, select
from typing import List, Optional
from src.models import Conversation, ConversationCreate


class ConversationService:
    def create_conversation(self, db_session: Session, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation.from_orm(conversation_data)
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, db_session: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """Get a specific conversation by ID for a user."""
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return db_session.exec(query).first()

    def get_conversations_by_user(self, db_session: Session, user_id: int) -> List[Conversation]:
        """Get all conversations for a user."""
        query = select(Conversation).where(Conversation.user_id == user_id)
        return db_session.exec(query).all()