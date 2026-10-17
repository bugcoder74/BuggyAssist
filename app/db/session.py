from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

db_name = "easyattend.db"
db_url = f"sqlite:///{db_name}"

engine = create_engine(db_url, echo = False)

def create_db_and_tables():
    """creates the tables of important models into the DB"""
    SQLModel.metadata.create_all(engine)
