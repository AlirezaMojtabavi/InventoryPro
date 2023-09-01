from sqlalchemy import Column, Integer, LargeBinary
from .Base import Base


class ProductImage(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, nullable=False)
    image = Column(LargeBinary)
