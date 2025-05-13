from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class AgentRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    scenario_id: UUID

class AgentRoleCreate(AgentRoleBase):
    pass

class AgentRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None

class AgentRoleInDBBase(AgentRoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AgentRoleDTO(AgentRoleInDBBase):
    pass