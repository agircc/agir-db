from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ProcessRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    process_id: UUID

class ProcessRoleCreate(ProcessRoleBase):
    pass

class ProcessRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None

class ProcessRoleInDBBase(ProcessRoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ProcessRoleDTO(ProcessRoleInDBBase):
    pass 