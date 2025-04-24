from datetime import datetime
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

# Common base schemas
class CapabilityBase(BaseModel):
    name: str
    description: Optional[str] = None


# Base schema for user capability
class UserCapabilityBase(BaseModel):
    name: str
    description: Optional[str] = None
    proficiency_level: float = Field(ge=1.0, le=5.0, default=1.0)
    years_experience: Optional[float] = None


# Schemas for creating items
class CapabilityCreate(CapabilityBase):
    pass


# Schema for creating a new capability
class UserCapabilityCreate(UserCapabilityBase):
    pass


# Schema for updating items
class CapabilityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Schema for updating a capability
class UserCapabilityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    proficiency_level: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    years_experience: Optional[float] = None


# Schemas for reading items
class Capability(CapabilityBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    created_by: uuid.UUID

    class Config:
        from_attributes = True


# Schema for providing feedback on a capability
class CapabilityFeedback(BaseModel):
    feedback_score: float = Field(ge=0.0, le=1.0, description="Feedback score between 0 and 1")
    task_id: uuid.UUID = Field(description="The task ID related to this feedback")
    notes: Optional[str] = None


# Schema for detailed capability view
class UserCapabilityDetail(UserCapabilityBase):
    id: uuid.UUID
    user_id: uuid.UUID
    confidence_score: float
    success_count: int
    failure_count: int
    feedback_count: int
    last_feedback_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Schema for basic capability view
class UserCapabilityBasic(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    proficiency_level: float
    confidence_score: float
    
    class Config:
        from_attributes = True


# Schema for task history entry
class TaskHistoryEntry(BaseModel):
    feedback: float
    timestamp: str


# Schema for user with all capabilities
class UserWithCapabilities(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    capabilities: List[UserCapabilityDetail] = []
    
    class Config:
        from_attributes = True


# Schema for capability statistics
class CapabilityStats(BaseModel):
    capability_name: str
    avg_proficiency: float
    user_count: int
    top_users: List[Dict[str, Any]] = [] 