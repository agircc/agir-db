from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from agir_db.schemas.state_role import StateRoleDTO
from agir_db.schemas.agent_role import AgentRoleDTO

class StateBase(BaseModel):
    scenario_id: UUID
    name: str
    description: Optional[str] = None
    prompt: Optional[str] = None
    node_type: Optional[str] = None

class StateCreate(StateBase):
    pass

class StateUpdate(StateBase):
    pass

class StateInDBBase(StateBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class StateDTO(StateInDBBase):
    state_roles: Optional[List[StateRoleDTO]] = []
    roles: Optional[List[AgentRoleDTO]] = [] 