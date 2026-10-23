from pydantic import BaseModel
from typing import List, Optional

# --- Login Schemas (Same as before) ---
class CyberVidyaLoginRequest(BaseModel):
    userName: str
    password: str

class CyberVidyaLoginData(BaseModel):
    id: int
    token: str
    hdr_auth: str
    auth_pref: str

class CyberVidyaLoginResponse(BaseModel):
    data: CyberVidyaLoginData
    message: str
    version: str

# --- Naye Registered Courses Schemas ---

class CourseCompDetail(BaseModel):
    courseCompId: int
    courseCompName: str
    presentLecture: int
    totalLecture: int
    # Hum sirf attendance ke liye zaroori fields le rahe hain

class RegisteredCourse(BaseModel):
    courseId : int
    courseName: str
    courseCode: str
    studentCourseCompDetails: List[CourseCompDetail]

class RegisteredCoursesResponse(BaseModel):
    data: List[RegisteredCourse]
    message: str
    version: str