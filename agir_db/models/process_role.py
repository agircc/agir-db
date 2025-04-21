from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from uuid import uuid4

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
    
    # Relationship to ProcessNodes
    nodes = relationship("ProcessNode", back_populates="role", cascade="all, delete-orphan") 