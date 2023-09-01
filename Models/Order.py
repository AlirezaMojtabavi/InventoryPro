from sqlalchemy import Column, Integer, Float, Date, String, Double
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer')
    order_time = Column(Date, default=datetime.now())
    totalPrice = Column(Float, default=0)

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.order_time = datetime.now()

