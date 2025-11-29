from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .Base import Base
from Setting import settings
from sqlalchemy import Enum as SAEnum


class Category(enum.Enum):
    Cat1 = settings.CAT1_NAME
    Cat2 = settings.CAT2_NAME
    Cat3 = settings.CAT3_NAME
    Cat4 = settings.CAT4_NAME
    Cat5 = settings.CAT5_NAME
    Delivery = 'Delivery'


class SubCat1(enum.Enum):
    SubCat1_1 = settings.SUB_CAT1_NAME_1
    SubCat1_2 = settings.SUB_CAT1_NAME_2
    SubCat1_3 = settings.SUB_CAT1_NAME_3
    SubCat1_4 = settings.SUB_CAT1_NAME_4


class SubCat2(enum.Enum):
    Armenia = 'Armenia'
    European = 'European'
    Arabic = 'Arabic'
    Russian = 'Russian'


class SubCat3(enum.Enum):
    Japanese = 'Japanese'
    European = 'European'
    Indonesian = 'Indonesian'
    Italian = 'Italian'
    Armenia = 'Armenia'


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    price = Column(Float, nullable=False, default=0.0)
    label = Column(SAEnum(Category, values_callable=lambda x: [e.value for e in x], native_enum=True,
                          create_type=False), default=Category.Cat5, nullable=False)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=True)
    image = relationship('ProductImage')

    def __init__(self, name, code, label=None, price=None):
        self.name = name
        self.code = code
        self.price = price or 0.0

        if isinstance(label, Category):
            self.label = label

        elif isinstance(label, str):
            try:
                self.label = Category[label]
            except KeyError:
                try:
                    self.label = Category(label)
                except ValueError:
                    self.label = Category.Cat5
        else:
            self.label = Category.Cat5

    def __str__(self):
        return self.name
