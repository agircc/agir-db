from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

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