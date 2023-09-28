from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .Base import Base


class Category(enum.Enum):
    Iqos = 'Iqos'
    Heets = 'Heets'
    Terea = 'Terea'
    Accessories = 'Accessories'
    Miscellaneous = 'Miscellaneous'
    Delivery = 'Delivery'


class HeetsCategory(enum.Enum):
    Armenia = 'Armenia'
    European = 'European'
    Arabic = 'Arabic'
    Russian = 'Russian'


class TereaCategory(enum.Enum):
    Japanese = 'Japanese'
    European = 'European'
    Indonesian = 'Indonesian'
    Italian = 'Italian'


class IqosCategory(enum.Enum):
    Iluma = 'Iluma'
    Lil = 'Lil'
    duo_3 = '3 duo'
    Originals_duo = 'Originals duo'


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    label = Column(Enum(Category), default=Category.Miscellaneous, nullable=False)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=True)
    image = relationship('ProductImage')


    def __init__(self, name, code, label=None, price=None):
        self.name = name
        self.code = code
        self.price = price

        if label is None:
            self.label = Category.Miscellaneous
        else:
            try:
                self.label = Category(label)
            except ValueError:
                self.label = Category.Miscellaneous

    def __str__(self):
        return self.name
