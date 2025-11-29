from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Product, Customer, OrderRow, Order, ProductImage
from Setting import settings

engine = create_engine(settings.DB_CONNECTION_STRING)

# Create tables (if not already created)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



