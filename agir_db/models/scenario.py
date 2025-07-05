from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base
from agir_db.models.assistant import Assistant
# from agir_db.models.state import State
# from agir_db.models.state_transition import StateTransition
# from agir_db.models.agent_role import AgentRole

class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    learner_role: Mapped[str] = mapped_column(String(100), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_user: Mapped["User"] = relationship("User")
    states: Mapped[List["State"]] = relationship("State", back_populates="scenario", cascade="all, delete-orphan")
    transitions: Mapped[List["StateTransition"]] = relationship("StateTransition", back_populates="scenario", cascade="all, delete-orphan")
    roles: Mapped[List["AgentRole"]] = relationship("AgentRole", back_populates="scenario", cascade="all, delete-orphan")
