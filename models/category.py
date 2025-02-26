from sqlalchemy import Column, Integer, String

from db import Base


class Category(Base):
    """Модель категории."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
