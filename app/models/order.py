from sqlalchemy import Column, Integer, String, ForeignKey,Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.db.base import Base


class OrderStatusEnum(str, Enum):
    CREATED = "CREATED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    status = Column(SQLEnum(OrderStatusEnum), default=OrderStatusEnum.CREATED)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")
