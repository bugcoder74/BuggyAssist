from pydantic import BaseModel
from typing import List

# Jo data client bhejega ya Mapper create karega
class SubjectCreate(BaseModel):
    name: str
    code: str  
    total_classes: int = 0
    attended_classes: int = 0

# Jo data client ko wapas milega (Read)
class SubjectRead(BaseModel):
    id: int
    name: str
    code: str
    total_classes: int
    attended_classes: int

    class Config:
        from_attributes = True

# Sync ke liye request schema
class SubjectSyncRequest(BaseModel):
    username: str
    password: str

# Sync ke liye response schema
class SyncResponse(BaseModel):
    sync_successful: bool
    message: str
    subjects: List[SubjectRead]