from datetime import datetime
import uuid
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from agir_db.models.organization import OrganizationType


# Shared properties
class OrganizationBase(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    organization_type: Optional[str] = OrganizationType.COMPANY
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=500)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_place_id: Optional[str] = Field(None, max_length=255)
    google_place_data: Optional[Dict[str, Any]] = None
    business_hours: Optional[Dict[str, Any]] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    price_level: Optional[int] = Field(None, ge=0, le=4)
    parent_id: Optional[uuid.UUID] = None
    is_active: bool = True
    is_verified: bool = False
    extra_data: Optional[Dict[str, Any]] = None


# Properties to receive via API on creation
class OrganizationCreate(OrganizationBase):
    name: str = Field(..., max_length=255)  # Required for creation


# Properties to receive via API on update
class OrganizationUpdate(OrganizationBase):
    pass


# Properties shared by models stored in DB
class OrganizationInDBBase(OrganizationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


# Properties to return to client
class OrganizationDTO(OrganizationInDBBase):
    pass


# Properties to return with hierarchical information
class OrganizationDetail(OrganizationDTO):
    parent: Optional["OrganizationBrief"] = None
    children: List["OrganizationBrief"] = []
    hierarchy_path: Optional[str] = None

    class Config:
        from_attributes = True


# Brief organization info for nested relationships
class OrganizationBrief(BaseModel):
    id: uuid.UUID
    name: str
    organization_type: str
    is_active: bool

    class Config:
        from_attributes = True


# For hierarchy tree representation
class OrganizationTree(OrganizationBrief):
    children: List["OrganizationTree"] = []

    class Config:
        from_attributes = True


# For search and listing
class OrganizationList(BaseModel):
    organizations: List[OrganizationDTO]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

    class Config:
        from_attributes = True


# For Google Place API integration
class GooglePlaceInfo(BaseModel):
    place_id: str
    name: str
    formatted_address: Optional[str] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    price_level: Optional[int] = None
    types: List[str] = []
    opening_hours: Optional[Dict[str, Any]] = None
    geometry: Optional[Dict[str, Any]] = None
    photos: List[Dict[str, Any]] = []
    reviews: List[Dict[str, Any]] = []


# For bulk operations
class OrganizationBulkCreate(BaseModel):
    organizations: List[OrganizationCreate]


class OrganizationBulkUpdate(BaseModel):
    updates: List[Dict[str, Any]]  # List of {id: UUID, data: OrganizationUpdate}


# For search filters
class OrganizationSearchFilters(BaseModel):
    name: Optional[str] = None
    organization_type: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    has_google_place: Optional[bool] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


# Enable forward references
OrganizationDetail.model_rebuild()
OrganizationTree.model_rebuild() 