from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ProcessInstanceStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"

class ProcessInstanceBase(BaseModel):
    process_id: UUID
    current_node_id: Optional[UUID] = None
    initiator_id: UUID
    status: ProcessInstanceStatus = ProcessInstanceStatus.RUNNING

class ProcessInstanceCreate(ProcessInstanceBase):
    pass

class ProcessInstanceUpdate(BaseModel):
    current_node_id: Optional[UUID] = None
    status: Optional[ProcessInstanceStatus] = None

class ProcessInstanceInDBBase(ProcessInstanceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class ProcessInstance(ProcessInstanceInDBBase):
    pass
