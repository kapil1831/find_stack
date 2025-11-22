from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.find_stack.settings import settings
from collections.abc import Generator
from src.models.movie import Base

engine = create_engine(settings.database_url, echo=True, future=True)

def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session