from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# "SQL CREATE TABLE", database shape

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    brand = Column(String)
    category = Column(String)
    retailer = Column(String)
    url = Column(String, unique=True)
    tags = Column(String)
    created_at = Column(DateTime, server_default=func.now())



class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    event_type = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    product = relationship("Product")
