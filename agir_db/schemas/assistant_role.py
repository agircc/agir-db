from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AssistantRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    scenario_id: UUID

class AssistantRoleCreate(AssistantRoleBase):
    pass

class AssistantRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None

class AssistantRoleInDBBase(AssistantRoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AssistantRoleDTO(AssistantRoleInDBBase):
    pass