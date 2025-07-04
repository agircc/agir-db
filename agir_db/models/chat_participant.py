from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base


class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_conversations.id"), nullable=False)
    assistant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_read_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    conversation = relationship("ChatConversation", back_populates="participants")
    assistant = relationship("Assistant", foreign_keys=[assistant_id], back_populates="chat_participations")
    
    # Add a unique constraint to ensure an assistant can only be in a conversation once
    __table_args__ = (
        UniqueConstraint('conversation_id', 'assistant_id', name='uq_participant_conversation_assistant'),
    ) 