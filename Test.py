from Models.Product import Product
from Models.Customer import Customer
from Models.Order import Order
from Models.OrderRow import OrderRow
from datetime import datetime
import pandas as pd
from database import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
# -----------------------------------------------------------------------
# ------------------- To initialize the table of Product--------------------
# Read the Excel file
# df = pd.read_excel('Product specifications.xlsx')
# #Extract the product names from the first column
# product_names = df.iloc[:, 0].tolist()
# product_codes = df.iloc[:, 1].tolist()
# Product.insert_items(product_names, product_codes)
# ------------------------------------------------------------------------
# customer = Customer.create_new_customer("first_customer", "09124042512")
# rows = []
# order = Order.create_new_order(customer_id=customer.id)
# order_row1 = OrderRow(order_id=order.id, product_id=1, quantity=2)
# rows.append(order_row1)
# order_row2 = OrderRow(order_id=order.id, product_id=2, quantity=3)
# rows.append(order_row2)
# order.add_order_rows(rows)
#
# hola = 'salam'
# ------------------------------------------------------------------------

customer = Customer(name='John Doe', phone='1234567890', address='123 Main St')
#order = Order(customer=customer)
order = Order.create_new_order(customer_id=customer.id)

rows = []
order_row1 = OrderRow(order_id=order.id, product_id=1, quantity=2)
order_row2 = OrderRow(order_id=order.id, product_id=2, quantity=3)
order_rows = order.rows
rows.append(order_row1)
rows.append(order_row2)
order.add_order_rows(rows)

with Session() as session:
    # Create a new order and pass the customer ID explicitly
    session.add(order)
    session.commit()
    session.close()

    hola = 1
order_rows = order.rows

# Print the customer, order, and order rows
print("Customer:", customer.name)
print("Order ID:", order.id)
print("Order Rows:")
for order_row in order_rows:
    print("Product ID:", order_row.product_id, "Quantity:", order_row.quantity)