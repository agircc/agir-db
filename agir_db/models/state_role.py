from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, DateTime
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