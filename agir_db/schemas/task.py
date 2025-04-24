from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, root_validator

from app.models.task import TaskStatus
from app.schemas.file import FileUploadResponse
from app.schemas.user import User


# Base Pydantic models
class TaskCommentBase(BaseModel):
    content: str


class TaskAttachmentBase(BaseModel):
    file_name: str
    file_url: str
    file_size: int
    mime_type: str


# File upload response from frontend
class FileUploadResponse(BaseModel):
    filename: str
    content_type: str
    url: str
    size: int


# Base schema for Task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    parent_id: Optional[UUID] = None


# Create Pydantic models
class TaskCommentCreate(TaskCommentBase):
    task_id: UUID


class TaskAttachmentCreate(TaskAttachmentBase):
    task_id: UUID


# Schema for Task creation
class TaskCreate(TaskBase):
    assigned_to: Optional[UUID] = None
    attachments: Optional[List[FileUploadResponse]] = None


# Update Pydantic models
class TaskCommentUpdate(BaseModel):
    content: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    parent_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None


# DB Read Pydantic models
class TaskCommentInDB(TaskCommentBase):
    id: UUID
    task_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TaskAttachmentInDB(TaskAttachmentBase):
    id: UUID
    task_id: UUID
    user_id: UUID
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AssigneeInfo(BaseModel):
    user_id: UUID
    assigned_at: Optional[datetime] = None
    assigned_by: Optional[UUID] = None
    
    model_config = ConfigDict(from_attributes=True)


class TaskInDB(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    assigned_to: Optional[UUID] = None
    assigned_by: Optional[UUID] = None
    assigned_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Response Pydantic models
class TaskBrief(BaseModel):
    id: UUID
    title: str
    status: TaskStatus
    
    model_config = ConfigDict(from_attributes=True)


class TaskComment(TaskCommentInDB):
    pass


class TaskAttachment(TaskAttachmentInDB):
    pass


class Task(TaskInDB):
    subtasks: List[TaskBrief] = []
    
    model_config = ConfigDict(from_attributes=True)


class TaskDetail(TaskInDB):
    parent: Optional["TaskDetail"] = None
    subtasks: List["TaskDetail"] = []
    comments: List["TaskComment"] = []
    attachments: List["TaskAttachment"] = []
    
    owner: Optional[User] = None
    assigned_to_user: Optional[User] = None
    assigned_by_user: Optional[User] = None
    
    model_config = ConfigDict(from_attributes=True)


# List response models
class TaskList(BaseModel):
    items: List[Task]
    total: int
    
    model_config = ConfigDict(from_attributes=True)


class TaskCommentList(BaseModel):
    items: List[TaskComment]
    total: int
    
    model_config = ConfigDict(from_attributes=True)


class TaskAttachmentList(BaseModel):
    items: List[TaskAttachment]
    total: int
    
    model_config = ConfigDict(from_attributes=True)


class TaskCountSummary(BaseModel):
    """Summary counts of tasks by status"""
    todo: int = 0
    in_progress: int = 0
    review: int = 0
    done: int = 0
    archived: int = 0
    total: int = 0
    
    model_config = ConfigDict(from_attributes=True) 