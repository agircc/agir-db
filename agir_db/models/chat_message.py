from datetime import datetime
import uuid
import enum
from typing import Optional
from sqlalchemy import Column, Text, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base


class MessageStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_conversations.id"), nullable=False)
    sender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Enum(MessageStatus, native_enum=False), default=MessageStatus.SENT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("ChatConversation", back_populates="messages")
    sender = relationship("Assistant", foreign_keys=[sender_id], back_populates="chat_messages")
    
    # Optional reply to another message
    reply_to_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("chat_messages.id"), nullable=True)
    replies = relationship("ChatMessage", 
                          back_populates="reply_to",
                          foreign_keys=[reply_to_id])
    reply_to = relationship("ChatMessage", 
                          back_populates="replies",
                          remote_side=[id],
                          foreign_keys=[reply_to_id]) 