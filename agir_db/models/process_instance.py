from datetime import datetime
import uuid
import enum
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base

class ProcessInstanceStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"

class ProcessInstance(Base):
    __tablename__ = "process_instances"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    process_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processes.id"), nullable=False, index=True)
    current_node_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("process_nodes.id"), nullable=True)
    initiator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(Enum(ProcessInstanceStatus, native_enum=False), default=ProcessInstanceStatus.RUNNING, nullable=False)
    config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    evolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    process = relationship("Process")
    current_node = relationship("ProcessNode")
    initiator = relationship("User")
    role_users: Mapped[List["ProcessRoleUser"]] = relationship("ProcessRoleUser", back_populates="process_instance")
