from sqlmodel import Session, select
from typing import List
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate

def upsert_subjects(session: Session, subjects_data: List[SubjectCreate]) -> List[Subject]:
    """
    Subjects ko update karta hai agar code match kare, warna naya insert karta hai.
    """
    upserted_subjects = [] # update or insert = upsert
    for data in subjects_data:
        # Check if subject with this unique code already exists
        statement = select(Subject).where(Subject.code == data.code)
        existing_subject = session.exec(statement).first()
        
        if existing_subject:
            # Update existing record
            existing_subject.name = data.name
            existing_subject.total_classes = data.total_classes
            existing_subject.attended_classes = data.attended_classes
            session.add(existing_subject)
            upserted_subjects.append(existing_subject)
        else:
            # Create new record
            new_subject = Subject(
                name=data.name,
                code=data.code,
                total_classes=data.total_classes,
                attended_classes=data.attended_classes
            )
            session.add(new_subject)
            upserted_subjects.append(new_subject)
    
    session.commit()
    
    # IDs aur latest data wapas lane ke liye refresh karein
    for subj in upserted_subjects:
        session.refresh(subj)
        
    return upserted_subjects

def get_all_subjects(session: Session) -> List[Subject]:
    return session.exec(select(Subject)).all()