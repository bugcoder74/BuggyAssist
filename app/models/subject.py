from sqlmodel import SQLModel, Field
from typing import Optional

class Subject(SQLModel, table=True):

    id : Optional[int] = Field(
        default = None,
        primary_key = True
    )

    name : str = Field(
        index = True
    )

    code : str = Field(
        default = ""
    )

    total_classes : int = Field(
        default = 0
    )

    attended_classes : int = Field(
        default = 0
    )
    