from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class EpisodeStatus(str, Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"

class EpisodeBase(BaseModel):
    scenario_id: UUID
    current_state_id: Optional[UUID] = None
    initiator_id: UUID
    status: EpisodeStatus = EpisodeStatus.RUNNING
    config: Optional[Dict[str, Any]] = None
    evolution: Optional[str] = None

class EpisodeCreate(EpisodeBase):
    pass

class EpisodeUpdate(BaseModel):
    current_state_id: Optional[UUID] = None
    status: Optional[EpisodeStatus] = None
    config: Optional[Dict[str, Any]] = None
    evolution: Optional[str] = None

class EpisodeInDBBase(EpisodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class EpisodeDTO(EpisodeInDBBase):
    pass
