from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://admin:secret@db:5432/mydatabase"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Создает и предоставляет сессию базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
