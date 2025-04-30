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


class ChatParticipantBase(BaseModel):
    user_id: UUID


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
class ChatUserBrief(BaseModel):
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
    sender: Optional[ChatUserBrief] = None
    
    class Config:
        from_attributes = True


class ChatParticipantResponse(ChatParticipantBase):
    id: UUID
    conversation_id: UUID
    is_active: bool
    joined_at: datetime
    last_read_at: Optional[datetime] = None
    user: Optional[ChatUserBrief] = None
    
    class Config:
        from_attributes = True


class ChatConversationResponse(ChatConversationBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    created_by: UUID
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
    last_message: Optional[ChatMessageResponse] = None
    unread_count: int = 0
    participants: List[ChatParticipantResponse] = []
    
    class Config:
        from_attributes = True 