from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Product(Base):
    """Модель продукта."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))

    category = relationship("Category")
    shop = relationship("Shop")
