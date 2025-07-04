from enum import Enum
from typing import Dict, List
from pydantic import BaseModel

from agir_db.models.assistant import LLMModel, EmbeddingModel


class ModelCategory(str, Enum):
    LLM = "llm"
    EMBEDDING = "embedding"


class ModelInfo(BaseModel):
    id: str
    name: str
    value: str
    category: ModelCategory
    provider: str


class ModelsResponse(BaseModel):
    llm_models: List[ModelInfo]
    embedding_models: List[ModelInfo] 