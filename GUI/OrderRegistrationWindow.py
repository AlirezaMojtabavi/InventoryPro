from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from GUI.CustomerRegistrationWidget import CustomerRegistrationWidget
from GUI.ProductsOrderingWidget import ProductsOrderingWidget


class OrderRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.customer_Registration_widget = None
        self.product_ordering_widget = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        customer_section_label = QLabel("Customer Registration")
        self.customer_Registration_widget = CustomerRegistrationWidget()
        self.customer_Registration_widget.customer_confirmation_button.clicked.connect(self.show_product_ordering_widget)
        layout.addWidget(customer_section_label)
        layout.addWidget(self.customer_Registration_widget)

        self.product_ordering_widget = ProductsOrderingWidget()
        self.product_ordering_widget.setDisabled(True)
        layout.addWidget(self.product_ordering_widget)
        self.setLayout(layout)

        self.setWindowTitle('Customer Registration Window')
        self.setGeometry(100, 100, 500, 450)

        # self.ProductsSection = ProductsSection()
        # self.product_ordering_widget.hide()
        # self.layout.addWidget(self.product_ordering_widget)
        #
        # self.setLayout(self.layout)

    def show_product_ordering_widget(self):
        order_repository = self.customer_Registration_widget.get_order_repository()
        self.product_ordering_widget.set_order_repository(order_repository)
        self.product_ordering_widget.setDisabled(False)
        self.product_ordering_widget.show()
