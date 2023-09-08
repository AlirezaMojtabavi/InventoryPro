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


    # def remove_product(self, product, amount=None):
    #
    #     if self.status == 1:
    #         p = Product.objects.get(id=product.id)
    #         row = self.rows.get(product_id=p.id, order_id=self.id, order__customer_id=self.customer.id)
    #         if not row.exist():
    #             raise ValueError("This Product doesn't exist in the Customer's row ")
    #         else:
    #             amount_of_row = row.amount
    #             if (amount is None) or (amount == amount_of_row):
    #                 p.increase_inventory(amount_of_row)
    #                 # self.customer.deposit(p.price * amount_of_row)
    #                 self.total_price -= p.price * amount_of_row
    #                 row.delete()
    #                 self.save()

    # STATUS_SHOPPING = 1
    # STATUS_SUBMITTED = 2
    # STATUS_CANCELED = 3
    # STATUS_SENT = 4
    # choice_status = (
    #    (STATUS_SHOPPING, 'در حال خرید'),
    #    (STATUS_SUBMITTED, 'ثبت‌شده'),
    #    (STATUS_CANCELED, 'لغوشده'),
    #    (STATUS_SENT, 'ارسال‌شده'),
    # )
    # status = Integer(choices=choice_status)

    #

    #
    #
    # def submit(self):
    #     if (self.status == 1) and (self.total_price != 0):
    #         self.status = 2
    #         self.save()
    #     else:
    #         raise ValidationError("For using 'submit', status must be 1 and rows not to be empty")
    #
    # def cancel(self):
    #     if self.status == 2:
    #
    #         rows = self.rows.filter(order_id=self.id, order__customer_id=self.customer.id)
    #         for row in rows:
    #             p = Product.objects.get(id=row.product_id)
    #             amount = row.amount
    #             #self.customer.deposit(p.price * amount)
    #             p.increase_inventory(amount)
    #             self.total_price -= p.price * amount
    #             row.delete()
    #
    #         self.status = 3
    #         self.save()
    #     else:
    #         raise ValidationError("For using 'cancel', status must be 2")
    #
    # def send(self):
    #     if self.status == 2:
    #         if self.total_price == 0:
    #             self.status = 3
    #         else:
    #             self.status = 4
    #         self.save()
    #     else:
    #         raise ValidationError("For using 'send', status must be 2")
