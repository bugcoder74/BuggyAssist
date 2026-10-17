from sqlmodel import Session, select
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate

def create_subject(session:Session, subject_data: SubjectCreate) -> Subject:
    db_subject = Subject(
        name = subject_data.name
    )

    session.add(db_subject)
    session.commit()
    session.refresh(db_subject)
    return db_subject

def get_all_subjects(session: Session) -> list[Subject]:
    return session.exec(select(Subject)).all()
