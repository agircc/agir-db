from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from agir_db.schemas.process_role import ProcessRoleDTO

class ProcessBase(BaseModel):
    name: str
    learner_role: str
    description: Optional[str] = None
    created_by: UUID

class ProcessCreate(ProcessBase):
    pass

class ProcessUpdate(ProcessBase):
    pass

class ProcessNodeRoleBase(BaseModel):
    process_node_id: UUID
    process_role_id: UUID

class ProcessNodeRoleCreate(ProcessNodeRoleBase):
    pass

class ProcessNodeRoleInDBBase(ProcessNodeRoleBase):
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProcessNodeRoleDTO(ProcessNodeRoleInDBBase):
    pass

class ProcessNodeBase(BaseModel):
    process_id: UUID
    name: str
    description: Optional[str] = None
    node_type: Optional[str] = None

class ProcessNodeCreate(ProcessNodeBase):
    pass

class ProcessNodeUpdate(ProcessNodeBase):
    pass

class ProcessNodeInDBBase(ProcessNodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ProcessNodeDTO(ProcessNodeInDBBase):
    node_roles: Optional[List[ProcessNodeRoleDTO]] = []
    roles: Optional[List[ProcessRoleDTO]] = []

class ProcessTransitionBase(BaseModel):
    process_id: UUID
    from_node_id: UUID
    to_node_id: UUID
    condition: Optional[str] = None

class ProcessTransitionCreate(ProcessTransitionBase):
    pass

class ProcessTransitionUpdate(ProcessTransitionBase):
    pass

class ProcessTransitionInDBBase(ProcessTransitionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ProcessTransitionDTO(ProcessTransitionInDBBase):
    pass

class ProcessInDBBase(ProcessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ProcessDTO(ProcessInDBBase):
    pass

class Process(ProcessInDBBase):
    nodes: Optional[List[ProcessNodeDTO]] = []
    transitions: Optional[List[ProcessTransitionDTO]] = []
    roles: Optional[List[ProcessRoleDTO]] = []
