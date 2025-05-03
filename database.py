from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base, Product, Customer, OrderRow, Order, ProductImage
import configparser
import sys


try:
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'Database' not in config or 'connection_string' not in config['Database']:
        raise KeyError("Missing 'connection_string' in the 'Database' section of config.ini")

    connection_string = config.get('Database', 'connection_string')

    engine = create_engine(connection_string)

    # Create tables
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Failed to create tables: {e}")
        sys.exit(1)

    Session = sessionmaker(bind=engine)

except (configparser.Error, KeyError) as config_err:
    print(f"Configuration error: {config_err}")
    sys.exit(1)

except Exception as db_err:
    print(f"Database connection error: {db_err}")
    sys.exit(1)


