from typing import Optional
from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    """
    Schema for file upload response sent from frontend
    """
    filename: str
    content_type: str
    url: str
    size: int
    
    class Config:
        from_attributes = True 