from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ProcessRoleUserBase(BaseModel):
    user_id: UUID
    role_id: UUID 
    process_instance_id: Optional[UUID] = None
    description: Optional[str] = None

class ProcessRoleUserCreate(ProcessRoleUserBase):
    pass

class ProcessRoleUserUpdate(BaseModel):
    description: Optional[str] = None
    process_instance_id: Optional[UUID] = None

class ProcessRoleUserInDBBase(ProcessRoleUserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ProcessRoleUserDTO(ProcessRoleUserInDBBase):
    pass 