from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import timezone, datetime

# The common blueprint
class StudentBase(SQLModel):

    name : Optional[str] = Field(
        default = None
    )

    email : Optional[str] = Field(
            default = None
        )

    course_name : Optional[str] = Field(
                default = None
            )

    phone : Optional[str] = Field(
        default = None
    )

    college : Optional[str] = Field(
        default = None
    )


# Actual Database
class Student(StudentBase, table = True):
    __tablename__ = "students"

    id : Optional[int] = Field(
        default = None,
        primary_key = True
    )

    hashed_password : str = Field(
        description="Bcrypt hashed password"
    )

    

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc)
        }
    )



