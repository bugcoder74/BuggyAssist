from pydantic import BaseModel, ConfigDict
from datetime import datetime

# for create / update - sent by client
class StudentCreate(BaseModel):
    name : str
    email : str
    phone : str
    college : str
    password : str
    course_name : str

# The data that the client recieves as response
class StudentRead(BaseModel):
    id : int
    name : str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)
