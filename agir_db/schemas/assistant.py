from datetime import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel, EmailStr

from agir_db.models.assistant import LLMModel, EmbeddingModel


# Shared properties
class AssistantBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    description: Optional[str] = None
    personality_traits: Optional[List[str]] = None
    background: Optional[str] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    is_active: bool = True
    llm_model: Optional[str] = None
    embedding_model: Optional[str] = None


# Properties to receive via API on creation
class AssistantCreate(AssistantBase):
    pass


# Properties to receive via API on update
class AssistantUpdate(AssistantBase):
    pass


# Properties shared by models stored in DB
class AssistantInDBBase(AssistantBase):
    id: uuid.UUID
    created_at: datetime
    created_by: Optional[uuid.UUID] = None
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssistantDTO(AssistantBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

# Properties to return to client
class Assistant(AssistantInDBBase):
    pass

# Properties stored in DB
class AssistantInDB(AssistantInDBBase):
    pass 