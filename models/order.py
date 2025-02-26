from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Order(Base):
    """Модель заказа."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shop_id = Column(Integer, ForeignKey("shops.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User")
    shop = relationship("Shop")
    product = relationship("Product")
