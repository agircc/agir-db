from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base
from agir_db.models.scenario import Scenario

class State(Base):
    __tablename__ = "states"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    scenario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scenarios.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    node_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., start, end, approval, etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="states")
    # Replace direct many-to-many with association object pattern
    state_roles: Mapped[List["StateRole"]] = relationship("StateRole", back_populates="state", cascade="all, delete-orphan")
    # Convenience property to access roles directly
    roles: Mapped[List["AgentRole"]] = relationship("AgentRole", secondary="state_roles", viewonly=True)
    outgoing_transitions: Mapped[List["StateTransition"]] = relationship("StateTransition", foreign_keys="StateTransition.from_state_id", back_populates="from_state")
    incoming_transitions: Mapped[List["StateTransition"]] = relationship("StateTransition", foreign_keys="StateTransition.to_state_id", back_populates="to_state") 