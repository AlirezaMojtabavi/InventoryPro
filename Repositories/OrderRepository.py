from Models.Order import Order
from Models.OrderRow import OrderRow
from Repositories.ProductRepository import ProductRepository


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
        order_row = OrderRow(self.order.id, product_id, quantity, row_price)
        self.order.totalPrice += row_price
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
