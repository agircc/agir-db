from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class ProcessRoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    process_id: UUID

class ProcessRoleCreate(ProcessRoleBase):
    pass

class ProcessRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model: Optional[str] = None

class ProcessRoleInDBBase(ProcessRoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProcessRoleDTO(ProcessRoleInDBBase):
    pass

# 导入放在文件末尾以避免循环引用
from agir_db.schemas.process import ProcessNodeRoleDTO, ProcessNodeDTO
class ProcessRoleWithNodes(ProcessRoleDTO):
    role_nodes: Optional[List[ProcessNodeRoleDTO]] = []
    nodes: Optional[List[ProcessNodeDTO]] = [] 