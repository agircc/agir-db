from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from agir_db.db.base_class import Base
from uuid import uuid4
from typing import List

class AgentRole(Base):
    __tablename__ = "agent_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    model = Column(String, nullable=True)  # AI model associated with this role
    
    # Foreign key to Scenario
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenarios.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship to Scenario
    scenario = relationship("Scenario", back_populates="roles")
    
    # Updated relationship to use the association object
    role_states = relationship("StateRole", back_populates="role", cascade="all, delete-orphan")
    # Convenience property to access nodes directly
    states = relationship("State", secondary="state_roles", viewonly=True)
    
    # Relationship to AgentAssignment
    users = relationship("AgentAssignment", back_populates="role") 