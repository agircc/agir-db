from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Float, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from agir_db.db.base_class import Base


class AssistantMemory(Base):
    """
    Model for storing long-term memories for assistant agents.
    These memories can include significant interactions, preferences, past actions, etc.
    """
    __tablename__ = "assistant_memories"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    assistant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # The memory content
    meta_data: Mapped[dict] = mapped_column(JSONB, default={})  # Additional metadata about the memory
    importance: Mapped[float] = mapped_column(Float, default=1.0)  # Importance score (higher = more important)
    source: Mapped[str] = mapped_column(Text, nullable=True)  # Source of the memory (e.g., task, chat, etc.)
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)  # ID of the source object
    embedding: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # Vector embedding for semantic search
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  # Whether the memory is active
    last_accessed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Last time memory was accessed
    access_count: Mapped[int] = mapped_column(Integer, default=0)  # Number of times memory was accessed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow, nullable=True)
    
    # Relationships
    assistant: Mapped["Assistant"] = relationship("Assistant", back_populates="memories") 