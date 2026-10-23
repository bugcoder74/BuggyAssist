from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class AttendanceRecord(SQLModel, table=True):
    __tablename__ = "attendancerecord"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_code: str = Field(index=True)
    lecture_date: date
    status: str
    topic_covered: Optional[str] = Field(default=None)
    faculty_name: Optional[str] = Field(default=None)
    time_slot: Optional[str] = Field(default=None)