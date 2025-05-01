from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base

class ProcessNodeRole(Base):
    __tablename__ = "process_node_roles"
    
    process_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("process_nodes.id", ondelete="CASCADE"), primary_key=True)
    process_role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("process_roles.id", ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships to both sides
    node: Mapped["ProcessNode"] = relationship("ProcessNode", back_populates="node_roles")
    role: Mapped["ProcessRole"] = relationship("ProcessRole", back_populates="role_nodes")

class Process(Base):
    __tablename__ = "processes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    learner_role: Mapped[str] = mapped_column(String(100), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    created_by_user: Mapped["User"] = relationship("User")
    nodes: Mapped[List["ProcessNode"]] = relationship("ProcessNode", back_populates="process", cascade="all, delete-orphan")
    transitions: Mapped[List["ProcessTransition"]] = relationship("ProcessTransition", back_populates="process", cascade="all, delete-orphan")
    roles: Mapped[List["ProcessRole"]] = relationship("ProcessRole", back_populates="process", cascade="all, delete-orphan")

class ProcessNode(Base):
    __tablename__ = "process_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    process_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processes.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    node_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., start, end, approval, etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    process: Mapped["Process"] = relationship("Process", back_populates="nodes")
    # Replace direct many-to-many with association object pattern
    node_roles: Mapped[List["ProcessNodeRole"]] = relationship("ProcessNodeRole", back_populates="node", cascade="all, delete-orphan")
    # Convenience property to access roles directly
    roles: Mapped[List["ProcessRole"]] = relationship("ProcessRole", secondary="process_node_roles", viewonly=True)
    outgoing_transitions: Mapped[List["ProcessTransition"]] = relationship("ProcessTransition", foreign_keys="ProcessTransition.from_node_id", back_populates="from_node")
    incoming_transitions: Mapped[List["ProcessTransition"]] = relationship("ProcessTransition", foreign_keys="ProcessTransition.to_node_id", back_populates="to_node")

class ProcessTransition(Base):
    __tablename__ = "process_transitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    process_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processes.id"), nullable=False, index=True)
    from_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("process_nodes.id"), nullable=False)
    to_node_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("process_nodes.id"), nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 可选，转移的条件表达式
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    process: Mapped["Process"] = relationship("Process", back_populates="transitions")
    from_node: Mapped["ProcessNode"] = relationship("ProcessNode", foreign_keys=[from_node_id], back_populates="outgoing_transitions")
    to_node: Mapped["ProcessNode"] = relationship("ProcessNode", foreign_keys=[to_node_id], back_populates="incoming_transitions")
