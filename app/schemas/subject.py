from pydantic import BaseModel

# Jo data client bhejega (Create/Update)
class SubjectCreate(BaseModel):
    name: str

# Jo data client ko wapas milega (Read)
class SubjectRead(BaseModel):
    id: int
    name: str
    total_classes: int
    attended_classes: int