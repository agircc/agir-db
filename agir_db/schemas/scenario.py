from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from agir_db.schemas.agent_role import AgentRoleDTO
from agir_db.schemas.state import StateDTO
from agir_db.schemas.state_transition import StateTransitionDTO

class ScenarioBase(BaseModel):
    name: str
    learner_role: str
    description: Optional[str] = None
    created_by: UUID

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(ScenarioBase):
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
