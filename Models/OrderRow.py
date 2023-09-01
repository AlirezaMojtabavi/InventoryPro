from sqlalchemy import Column, Integer, String, Double, Float, Date
from .Base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class OrderRow(Base):
    __tablename__ = "order_rows"
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', backref=backref('rows'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', backref=backref('order_rows'))
    quantity = Column(Integer)
    rowPrice = Column(Float, default=0)

    def __init__(self, order_id, product_id, quantity, row_price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.rowPrice = row_price

