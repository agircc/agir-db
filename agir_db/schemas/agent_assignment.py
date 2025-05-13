from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AgentAssignmentBase(BaseModel):
    user_id: UUID
    role_id: UUID 
    episode_id: Optional[UUID] = None
    description: Optional[str] = None

class AgentAssignmentCreate(AgentAssignmentBase):
    pass

class AgentAssignmentUpdate(BaseModel):
    description: Optional[str] = None
    episode_id: Optional[UUID] = None

class AgentAssignmentInDBBase(AgentAssignmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AgentAssignmentDTO(AgentAssignmentInDBBase):
    pass 