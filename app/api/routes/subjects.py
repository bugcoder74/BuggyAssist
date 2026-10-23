from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.dependencies import get_session
from app.schemas.subject import SubjectCreate, SubjectRead, SubjectSyncRequest, SyncResponse
from app.repositories import subject_repo
from app.services import sync_service

router = APIRouter()

@router.post("/", response_model=SubjectRead, status_code=201)
def create_subject(subject: SubjectCreate, session: Session = Depends(get_session)):
    return subject_repo.create_subject(session, subject)

@router.get("/", response_model=list[SubjectRead])
def read_subjects(session: Session = Depends(get_session)):
    return subject_repo.get_all_subjects(session)

@router.post("/sync", response_model=SyncResponse)
async def sync_subjects(
    request: SubjectSyncRequest, 
    session: Session = Depends(get_session)
):
    """
    CyberVidya se live data fetch karta hai. 
    Fail hone par local cached data return karta hai.
    """
    result = await sync_service.sync_attendance_data(
        session=session,
        username=request.username,
        password=request.password
    )
    return result