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
    discount = Column(Float, nullable=True, default=0.0)

    def __init__(self, order_id, product_id, row_price, quantity=None):
        self.order_id = order_id
        self.product_id = product_id
        self.rowPrice = row_price
        if quantity is not None:
            self.quantity = quantity
        else:
            self.quantity = 1
