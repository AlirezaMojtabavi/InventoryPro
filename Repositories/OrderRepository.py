from Models.Order import Order
from Models.OrderRow import OrderRow
from Repositories.ProductRepository import ProductRepository
from datetime import datetime


class OrderRepository:
    def __init__(self):
        from database import engine
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.order = None

    def create_new_order(self, customer_id):
        new_order = self.order = Order(customer_id=customer_id)
        self.session.add(self.order)
        self.session.commit()
        return new_order

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order

    def get_current_order_id(self):
        return self.order.id

    def add_row(self, product_id, quantity):
        product_repo = ProductRepository()
        row_price = product_repo.get_product_by_id(product_id).price * quantity
        order_row = OrderRow(order_id=self.order.id, product_id=product_id, row_price=row_price, quantity=quantity)
        self.order.totalPrice += row_price
        self.order.rows.append(order_row)
        self.session.commit()

    def add_delivery_row(self, price):
        product_repo = ProductRepository()
        product_id = product_repo.get_product_by_code("9999").id
        order_row = OrderRow(self.order.id, product_id, row_price=price)
        self.order.totalPrice += price
        self.order.rows.append(order_row)
        self.session.commit()

    def remove_row(self, row_id):
        order_row = self.session.query(OrderRow).filter_by(id=row_id).first()
        if order_row:
            self.order.totalPrice -= order_row.rowPrice
            self.session.delete(order_row)
            self.session.commit()

    def order_is_empty(self):
        if len(self.order.rows) > 0:
            return False
        else:
            return True

    def discounted_row(self, row_id, discounted_price):
        order_row = self.session.query(OrderRow).filter_by(id=row_id).first()
        old_price = order_row.rowPrice
        if order_row:
            order_row.rowPrice = discounted_price
            self.order.totalPrice -= old_price
            self.order.totalPrice += discounted_price
            self.session.commit()

    def finish(self):
        self.session.close_all()

    def check_order_id(self, order_id):
        order = self.session.query(Order).filter_by(id=order_id).first()
        if order is not None:
            self.set_order(order)
            return order
        else:
            return None

    def get_cutomer_name(self):
        return self.order.customer.name

    def get_custoemr_phone(self):
        return self.order.customer.phone

    def get_total_price(self):
        return self.order.totalPrice

    def update_order_time(self):
        self.order.order_time = datetime.now()
