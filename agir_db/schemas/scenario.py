from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from agir_db.schemas.agent_role import AgentRoleDTO

class ScenarioBase(BaseModel):
    name: str
    learner_role: str
    description: Optional[str] = None
    created_by: UUID

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(ScenarioBase):
    pass

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

class StateBase(BaseModel):
    scenario_id: UUID
    name: str
    description: Optional[str] = None
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

class StateTransitionBase(BaseModel):
    scenario_id: UUID
    from_state_id: UUID
    to_state_id: UUID
    condition: Optional[str] = None

class StateTransitionCreate(StateTransitionBase):
    pass

class StateTransitionUpdate(StateTransitionBase):
    pass

class StateTransitionInDBBase(StateTransitionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class StateTransitionDTO(StateTransitionInDBBase):
    pass

class ScenarioInDBBase(ScenarioBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ScenarioDTO(ScenarioInDBBase):
    pass

class Scenario(ScenarioInDBBase):
    states: Optional[List[StateDTO]] = []
    transitions: Optional[List[StateTransitionDTO]] = []
    roles: Optional[List[AgentRoleDTO]] = []
