from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ProcessInstanceStepBase(BaseModel):
    instance_id: UUID
    node_id: UUID
    user_id: UUID
    action: str
    comment: Optional[str] = None

class ProcessInstanceStepCreate(ProcessInstanceStepBase):
    pass

class ProcessInstanceStepInDBBase(ProcessInstanceStepBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True

class ProcessInstanceStepDTO(ProcessInstanceStepInDBBase):
    pass
