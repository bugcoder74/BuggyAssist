from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.dependencies import get_session
from app.schemas.subject import SubjectCreate, SubjectRead
from app.repositories import subject_repo

router = APIRouter()

@router.post("/", response_model=SubjectRead, status_code=201)
def create_subject(subject: SubjectCreate, session: Session = Depends(get_session)):
    return subject_repo.create_subject(session, subject)

@router.get("/", response_model=list[SubjectRead])
def read_subjects(session: Session = Depends(get_session)):
    return subject_repo.get_all_subjects(session)