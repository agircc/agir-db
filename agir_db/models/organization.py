from datetime import datetime
import uuid
import enum
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from agir_db.db.base_class import Base


class OrganizationType(str, enum.Enum):
    """Type of organization"""
    COMPANY = "company"
    BRANCH = "branch"
    SUBSIDIARY = "subsidiary"
    DEPARTMENT = "department"
    RESTAURANT = "restaurant"
    STORE = "store"
    MUSEUM = "museum"
    HOSPITAL = "hospital"
    SCHOOL = "school"
    HOTEL = "hotel"
    BANK = "bank"
    GAS_STATION = "gas_station"
    SHOPPING_MALL = "shopping_mall"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"


class Organization(Base):
    """Organization model that supports company info, Google Place data, and hierarchies"""
    __tablename__ = "organizations"
    
    # Basic fields
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization_type: Mapped[str] = mapped_column(String(50), nullable=False, default=OrganizationType.COMPANY)
    
    # Contact information
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Address information
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Location coordinates
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Google Place API specific fields
    google_place_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True, index=True)
    google_place_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Business information
    business_hours: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    price_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Hierarchical relationship - self-referencing foreign key
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True, index=True)
    
    # Status and metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Additional metadata for extensibility
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Relationships
    # Parent-child relationship for hierarchy
    parent: Mapped[Optional["Organization"]] = relationship("Organization", remote_side=[id], back_populates="children")
    children: Mapped[List["Organization"]] = relationship("Organization", back_populates="parent")
    
    # Relationship to user who created this organization
    creator: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', type='{self.organization_type}')>"
    
    def get_full_hierarchy_path(self) -> str:
        """Get the full hierarchy path from root to current organization"""
        path = [self.name]
        current = self.parent
        while current:
            path.insert(0, current.name)
            current = current.parent
        return " > ".join(path)
    
    def get_all_descendants(self) -> List["Organization"]:
        """Get all descendant organizations recursively"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants 