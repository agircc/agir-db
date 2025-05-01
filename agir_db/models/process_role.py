from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from agir_db.db.base_class import Base
from uuid import uuid4
from typing import List

class ProcessRole(Base):
    __tablename__ = "process_roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    model = Column(String, nullable=True)  # AI model associated with this role
    
    # Foreign key to Process
    process_id = Column(UUID(as_uuid=True), ForeignKey("processes.id", ondelete="CASCADE"), nullable=False)
    
    # Relationship to Process
    process = relationship("Process", back_populates="roles")
    
    # Updated relationship to use the association object
    role_nodes = relationship("ProcessNodeRole", back_populates="role", cascade="all, delete-orphan")
    # Convenience property to access nodes directly
    nodes = relationship("ProcessNode", secondary="process_node_roles", viewonly=True)
    
    # Relationship to ProcessRoleUser
    users = relationship("ProcessRoleUser", back_populates="role") 