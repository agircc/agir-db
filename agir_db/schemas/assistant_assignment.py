from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AssistantAssignmentBase(BaseModel):
    assistant_id: UUID
    role_id: UUID 
    episode_id: Optional[UUID] = None
    description: Optional[str] = None

class AssistantAssignmentCreate(AssistantAssignmentBase):
    pass

class AssistantAssignmentUpdate(BaseModel):
    description: Optional[str] = None
    episode_id: Optional[UUID] = None

class AssistantAssignmentInDBBase(AssistantAssignmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AssistantAssignmentDTO(AssistantAssignmentInDBBase):
    pass 