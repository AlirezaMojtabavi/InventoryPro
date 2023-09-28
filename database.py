from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Product, Customer, OrderRow, Order, ProductImage
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
connection_string = config.get('Database', 'connection_string')
engine = create_engine(connection_string)
#engine = create_engine('postgresql://postgres:22462006@localhost:5432/karen_database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


