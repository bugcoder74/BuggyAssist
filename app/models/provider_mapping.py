from sqlmodel import SQLModel, Field
from typing import Optional

class ProviderSubjectMapping(SQLModel, table=True):
    __tablename__ = "provider_subject_mapping"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_code: str = Field(index=True)
    provider_name: str = Field(index=True)
    external_course_id: int
    external_course_comp_id: int
    external_student_id: Optional[int] = Field(default=None)