from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from GUI.CustomerRegistrationWidget import CustomerRegistrationWidget
from GUI.ProductsOrderingWidget import ProductsOrderingWidget


class OrderRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.customer_Registration_widget = None
        self.product_ordering_widget = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.customer_Registration_widget = CustomerRegistrationWidget()
        self.customer_Registration_widget.customer_confirmation_button.clicked.connect(
            self.retrieve_order)
        self.layout.addWidget(self.customer_Registration_widget)
        self.setLayout(self.layout)
        self.setWindowTitle('Customer Registration Window')
        self.setGeometry(100, 60, 400, 180)

    def show_product_ordering_widget(self):
        self.product_ordering_widget.setDisabled(False)
        self.product_ordering_widget.show()

    def retrieve_order(self):
        order_repo = self.customer_Registration_widget.get_order_repository()
        self.product_ordering_widget = ProductsOrderingWidget(order_repo)
        #order_repo = self.customer_Registration_widget.get_order_repository()
        #self.product_ordering_widget.set_order_repository(order_repo)
        self.layout.addWidget(self.product_ordering_widget)
        self.setGeometry(100, 45, 750, 600)
        self.product_ordering_widget.show()
