from datetime import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel

from agir_db.models.assistant_organization import OrganizationRole


# Shared properties
class AssistantOrganizationBase(BaseModel):
    role: Optional[str] = OrganizationRole.MEMBER
    is_active: bool = True


# Properties to receive via API on creation
class AssistantOrganizationCreate(AssistantOrganizationBase):
    assistant_id: uuid.UUID
    organization_id: uuid.UUID


# Properties to receive via API on update
class AssistantOrganizationUpdate(AssistantOrganizationBase):
    pass


# Properties shared by models stored in DB
class AssistantOrganizationInDBBase(AssistantOrganizationBase):
    id: uuid.UUID
    assistant_id: uuid.UUID
    organization_id: uuid.UUID
    joined_at: datetime
    updated_at: datetime
    added_by: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


# Properties to return to client
class AssistantOrganizationDTO(AssistantOrganizationInDBBase):
    pass


# Brief assistant info for nested relationships
class AssistantBrief(BaseModel):
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


# For detailed responses with assistant and organization info
class AssistantOrganizationDetail(AssistantOrganizationDTO):
    assistant: Optional["AssistantBrief"] = None
    organization: Optional["OrganizationBrief"] = None
    added_by_assistant: Optional["AssistantBrief"] = None

    class Config:
        from_attributes = True


# For adding/removing assistants from organization
class OrganizationMembershipRequest(BaseModel):
    assistant_ids: List[uuid.UUID]
    role: Optional[str] = OrganizationRole.MEMBER


# For bulk operations
class AssistantOrganizationBulkCreate(BaseModel):
    memberships: List[AssistantOrganizationCreate]


# For organization members listing
class OrganizationMembersList(BaseModel):
    members: List[AssistantOrganizationDetail]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# For assistant organizations listing
class AssistantOrganizationsList(BaseModel):
    organizations: List[AssistantOrganizationDetail]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


# For invitation/join requests
class OrganizationInvitation(BaseModel):
    organization_id: uuid.UUID
    assistant_email: str
    role: Optional[str] = OrganizationRole.MEMBER
    message: Optional[str] = None


# For role changes
class RoleChangeRequest(BaseModel):
    assistant_id: uuid.UUID
    new_role: str


# Enable forward references
AssistantOrganizationDetail.model_rebuild() 