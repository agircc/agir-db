from datetime import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel

from agir_db.models.user_organization import OrganizationRole


# Shared properties
class UserOrganizationBase(BaseModel):
    role: Optional[str] = OrganizationRole.MEMBER
    is_active: bool = True


# Properties to receive via API on creation
class UserOrganizationCreate(UserOrganizationBase):
    user_id: uuid.UUID
    organization_id: uuid.UUID


# Properties to receive via API on update
class UserOrganizationUpdate(UserOrganizationBase):
    pass


# Properties shared by models stored in DB
class UserOrganizationInDBBase(UserOrganizationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    organization_id: uuid.UUID
    joined_at: datetime
    updated_at: datetime
    added_by: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


# Properties to return to client
class UserOrganizationDTO(UserOrganizationInDBBase):
    pass


# Brief user info for nested relationships
class UserBrief(BaseModel):
    id: uuid.UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool

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


# For detailed responses with user and organization info
class UserOrganizationDetail(UserOrganizationDTO):
    user: Optional["UserBrief"] = None
    organization: Optional["OrganizationBrief"] = None
    added_by_user: Optional["UserBrief"] = None

    class Config:
        from_attributes = True


# For adding/removing users from organization
class OrganizationMembershipRequest(BaseModel):
    user_ids: List[uuid.UUID]
    role: Optional[str] = OrganizationRole.MEMBER


# For bulk operations
class UserOrganizationBulkCreate(BaseModel):
    memberships: List[UserOrganizationCreate]


# For organization members listing
class OrganizationMembersList(BaseModel):
    members: List[UserOrganizationDetail]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# For user organizations listing
class UserOrganizationsList(BaseModel):
    organizations: List[UserOrganizationDetail]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# For invitation/join requests
class OrganizationInvitation(BaseModel):
    organization_id: uuid.UUID
    user_email: str
    role: Optional[str] = OrganizationRole.MEMBER
    message: Optional[str] = None


# For role changes
class RoleChangeRequest(BaseModel):
    user_id: uuid.UUID
    new_role: str


# Enable forward references
UserOrganizationDetail.model_rebuild() 