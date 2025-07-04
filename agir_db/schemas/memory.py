from datetime import datetime
import uuid
from typing import Dict, List, Optional, Any

from pydantic import BaseModel


# Base schema for UserMemory
class AssistantMemoryBase(BaseModel):
    content: str
    meta_data: Optional[Dict[str, Any]] = {}
    importance: Optional[float] = 1.0
    source: Optional[str] = None
    source_id: Optional[uuid.UUID] = None


# Schema for creating a new UserMemory
class AssistantMemoryCreate(AssistantMemoryBase):
    assistant_id: uuid.UUID


# Schema for updating an existing UserMemory
class AssistantMemoryUpdate(BaseModel):
    content: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    importance: Optional[float] = None
    is_active: Optional[bool] = None
    embedding: Optional[List[float]] = None


# Schema for UserMemory in response
class AssistantMemoryResponse(AssistantMemoryBase):
    id: uuid.UUID
    assistant_id: uuid.UUID
    is_active: bool
    access_count: int
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Schema for retrieving multiple UserMemory items with pagination
class AssistantMemoryList(BaseModel):
    items: List[AssistantMemoryResponse]
    total: int
    page: int
    page_size: int


# Schema for memory search parameters
class MemorySearchParams(BaseModel):
    query: str
    limit: Optional[int] = 10
    min_importance: Optional[float] = 0.0
    source: Optional[str] = None
    is_active: Optional[bool] = True 