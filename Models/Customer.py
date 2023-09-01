from sqlalchemy import Column, Integer, String
from .Base import Base


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    address = Column(String(150))

    def __init__(self, name, phone, address=None):
        self.name = name
        self.phone = phone
        if address is None:
            self.address = ""
        else:
            try:
                self.address = address
            except ValueError:
                self.address = ""

    def __str__(self):
        return self.name
