from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base

class StateRole(Base):
    __tablename__ = "state_roles"
    
    state_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("states.id", ondelete="CASCADE"), primary_key=True)
    agent_role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agent_roles.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships to both sides
    state: Mapped["State"] = relationship("State", back_populates="state_roles")
    role: Mapped["AgentRole"] = relationship("AgentRole", back_populates="role_states")

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

class StateTransition(Base):
    __tablename__ = "state_transitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    scenario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scenarios.id"), nullable=False, index=True)
    from_state_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("states.id"), nullable=False)
    to_state_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("states.id"), nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 可选，转移的条件表达式
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="transitions")
    from_state: Mapped["State"] = relationship("State", foreign_keys=[from_state_id], back_populates="outgoing_transitions")
    to_state: Mapped["State"] = relationship("State", foreign_keys=[to_state_id], back_populates="incoming_transitions")
