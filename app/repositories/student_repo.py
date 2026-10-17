from sqlmodel import Session, select
from app.models.student import Student
from app.schemas.student import StudentCreate

def create_student(session: Session, student_data: StudentCreate) -> Student:

    db_student = Student(
        name = student_data.name,
        email = student_data.email,
        phone = student_data.phone,
        course_name = student_data.course_name,
        college = student_data.college,
        hashed_password = student_data.password
    )

    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

def get_student(session: Session, id: int) -> Student | None:
    # session.get directly looks for the primary key
    return session.get(Student, id)