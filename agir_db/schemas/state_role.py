from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class StateRoleBase(BaseModel):
    state_id: UUID
    agent_role_id: UUID

class StateRoleCreate(StateRoleBase):
    pass

class StateRoleInDBBase(StateRoleBase):
    created_at: datetime
    
    class Config:
        from_attributes = True

class StateRoleDTO(StateRoleInDBBase):
    pass 