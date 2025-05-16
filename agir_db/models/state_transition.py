from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base
from agir_db.models.scenario import Scenario

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