from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class StepBase(BaseModel):
    episode_id: UUID
    state_id: UUID
    user_id: UUID
    action: str
    generated_text: Optional[str] = None

class StepCreate(StepBase):
    pass

class StepInDBBase(StepBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class StepDTO(StepInDBBase):
    pass
