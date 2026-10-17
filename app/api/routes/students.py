from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.dependencies import get_session
from app.schemas.student import StudentCreate, StudentRead
from app.repositories import student_repo

router = APIRouter()

@router.post("/", response_model=StudentRead, status_code=201)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student =  student_repo.create_student(session, student)
    return StudentRead.model_validate(db_student)

# @router.get("/", response_model=list[SubjectRead])
# def read_subjects(session: Session = Depends(get_session)):
#     return subject_repo.get_all_subjects(session)