from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from agir_db.models.chat_message import MessageStatus


# Base schemas for requests
class ChatMessageBase(BaseModel):
    content: str
    reply_to_id: Optional[UUID] = None


class ChatConversationBase(BaseModel):
    title: Optional[str] = None
    related_id: Optional[UUID] = None
    related_type: Optional[str] = None


class ChatParticipantBase(BaseModel):
    assistant_id: UUID


# Create schemas
class ChatMessageCreate(ChatMessageBase):
    conversation_id: UUID


class ChatConversationCreate(ChatConversationBase):
    participant_ids: List[UUID]


class ChatParticipantCreate(ChatParticipantBase):
    conversation_id: UUID


# Update schemas
class ChatMessageUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[MessageStatus] = None


class ChatConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ChatParticipantUpdate(BaseModel):
    is_active: Optional[bool] = None
    last_read_at: Optional[datetime] = None


# Response schemas
class ChatAssistantBrief(BaseModel):
    id: UUID
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChatMessageResponse(ChatMessageBase):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    status: MessageStatus
    created_at: datetime
    sender: Optional[ChatAssistantBrief] = None
    
    class Config:
        from_attributes = True


class ChatParticipantResponse(ChatParticipantBase):
    id: UUID
    conversation_id: UUID
    is_active: bool
    joined_at: datetime
    last_read_at: Optional[datetime] = None
    assistant: Optional[ChatAssistantBrief] = None
    
    class Config:
        from_attributes = True


class ChatConversationResponse(ChatConversationBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    related_id: Optional[UUID] = None
    related_type: Optional[str] = None
    participants: List[ChatParticipantResponse] = []
    
    class Config:
        from_attributes = True


class ChatConversationDetail(ChatConversationResponse):
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True


class UnreadMessageCount(BaseModel):
    conversation_id: UUID
    count: int


class ChatConversationBrief(BaseModel):
    id: UUID
    title: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    related_id: Optional[UUID] = None
    related_type: Optional[str] = None
    last_message: Optional[ChatMessageResponse] = None
    unread_count: int = 0
    participants: List[ChatParticipantResponse] = []
    
    class Config:
        from_attributes = True 