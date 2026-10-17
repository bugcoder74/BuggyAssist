from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import create_db_and_tables
from app.api.routes import health, subjects, students

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="EasyAttend API",
    description="Local-first attendance companion",
    version="0.2.0",
    lifespan=lifespan
)

# Routers ko plug-in ki tarah add karna
app.include_router(health.router)
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
app.include_router(students.router, prefix="/students", tags=["Students"])