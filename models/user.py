from datetime import datetime
import uuid
import enum
from typing import List
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class LLMModel(str, enum.Enum):
    # OpenAI models
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    
    # Anthropic models
    CLAUDE_3_HAIKU = "claude-3-haiku"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_5_SONNET = "claude-3.5-sonnet"
    CLAUDE_3_7_SONNET = "claude-3.7-sonnet"
    
    # Google models
    GEMINI_FLASH = "gemini-1.5-flash"
    GEMINI_PRO = "gemini-1.5-pro"
    
    # Meta models
    LLAMA_3_8B = "llama-3-8b"
    LLAMA_3_70B = "llama-3-70b"
    LLAMA_3_405B = "llama-3-405b"
    LLAMA_3_2_1B = "llama-3.2-1b"
    LLAMA_3_2_3B = "llama-3.2-3b"
    
    # Microsoft/OpenAI models
    GEMMA_2_9B = "gemma-2-9b"
    GEMMA_2_27B = "gemma-2-27b"


class EmbeddingModel(str, enum.Enum):
    # OpenAI models
    OPENAI_ADA_002 = "text-embedding-ada-002"
    OPENAI_3_SMALL = "text-embedding-3-small"
    OPENAI_3_LARGE = "text-embedding-3-large"
    
    # Cohere models
    COHERE_EMBED_ENGLISH = "embed-english-v3.0"
    COHERE_EMBED_MULTILINGUAL = "embed-multilingual-v3.0"
    
    # BAAI models
    BGE_SMALL = "bge-small-en-v1.5"
    BGE_BASE = "bge-base-en-v1.5"
    BGE_LARGE = "bge-large-en-v1.5"
    BGE_M3 = "bge-m3"
    
    # Jina models
    JINA_EMBED_V2 = "jina-embeddings-v2-base-en"
    JINA_EMBED_V2_SMALL = "jina-embeddings-v2-small-en"


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    last_login_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Use Enum directly instead of pre-defining ENUM type
    llm_model: Mapped[str] = mapped_column(Enum(LLMModel, native_enum=False), nullable=True, default=LLMModel.GPT_3_5_TURBO)
    embedding_model: Mapped[str] = mapped_column(Enum(EmbeddingModel, native_enum=False), nullable=True, default=EmbeddingModel.OPENAI_ADA_002)
    
    # Task relationships
    created_tasks: Mapped[List["Task"]] = relationship("Task", foreign_keys="Task.created_by", back_populates="owner")
    assigned_tasks: Mapped[List["Task"]] = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    task_comments: Mapped[List["TaskComment"]] = relationship("TaskComment", back_populates="user")
    task_attachments: Mapped[List["TaskAttachment"]] = relationship("TaskAttachment", back_populates="user")
    
    # User capability relationship
    capabilities: Mapped[List["UserCapability"]] = relationship("UserCapability", foreign_keys="UserCapability.user_id", back_populates="user")
    
    # User memory relationship
    memories: Mapped[List["UserMemory"]] = relationship("UserMemory", foreign_keys="UserMemory.user_id", back_populates="user") 