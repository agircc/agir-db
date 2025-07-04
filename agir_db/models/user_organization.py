from datetime import datetime
import uuid
import enum
from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from agir_db.db.base_class import Base


class OrganizationRole(str, enum.Enum):
    """Assistant role within an organization"""
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    GUEST = "guest"


class AssistantOrganization(Base):
    """Association model for Assistant-Organization many-to-many relationship"""
    __tablename__ = "assistant_organizations"
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    # Foreign keys
    assistant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=False, index=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    
    # Role and permissions
    role: Mapped[str] = mapped_column(String(50), nullable=False, default=OrganizationRole.MEMBER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Who added this assistant to the organization
    added_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assistants.id"), nullable=True)
    
    # Relationships
    assistant: Mapped["Assistant"] = relationship("Assistant", foreign_keys=[assistant_id], back_populates="organization_memberships")
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="assistant_memberships")
    added_by_assistant: Mapped[Optional["Assistant"]] = relationship("Assistant", foreign_keys=[added_by])
    
    def __repr__(self):
        return f"<AssistantOrganization(assistant_id={self.assistant_id}, org_id={self.organization_id}, role='{self.role}')>" 