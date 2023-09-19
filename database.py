from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Product, Customer, OrderRow, Order, ProductImage


engine = create_engine('postgresql://postgres:Aa123456@localhost:5432/karen_database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


