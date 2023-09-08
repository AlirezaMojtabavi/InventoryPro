from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QVBoxLayout, QFrame, QSpacerItem, \
    QSizePolicy, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt
from Repositories.CustomerRepository import CustomerRepository
from Repositories.OrderRepository import OrderRepository


class CustomerRegistrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.customer_confirmation_button = None
        self.phone_text = None
        self.name_text = None
        self.customer_repository = CustomerRepository()
        self.order_repository = OrderRepository()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        customer_group_box = QGroupBox("Customer Registration")
        customer_form_layout = QFormLayout()

        phone_label = QLabel("Phone Number:")
        self.phone_text = QLineEdit()
        self.phone_text.setFixedSize(100, 22)
        self.phone_text.returnPressed.connect(self.check_phone_number)
        customer_form_layout.addRow(phone_label, self.phone_text)

        name_label = QLabel("Name of Customer:")
        self.name_text = QLineEdit()
        self.name_text.setFixedSize(200, 22)
        self.name_text.returnPressed.connect(self.new_customer_registration)

        customer_form_layout.addRow(name_label, self.name_text)

        customer_group_box.setLayout(customer_form_layout)

        layout.addWidget(customer_group_box)

        self.customer_confirmation_button = QPushButton("Confirm the Customer")
        self.customer_confirmation_button.setFixedSize(120, 22)
        self.customer_confirmation_button.clicked.connect(self.enable_product_ordering_section)
        self.customer_confirmation_button.setEnabled(False)
        layout.addWidget(self.customer_confirmation_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def check_phone_number(self):
        phone_number = self.phone_text.text()
        if self.validate_phone_number(phone_number):
            if self.customer_repository.check_phone_number(phone_number):
                customer = self.customer_repository.get_customer_by_phone(phone_number)
                self.customer_repository.set_customer(customer)
                name = self.customer_repository.get_customer_name()
                self.name_text.setText(name)
                self.name_text.setDisabled(True)
                self.phone_text.setDisabled(True)
                self.customer_confirmation_button.setEnabled(True)
                self.customer_confirmation_button.setFocus()
            else:
                self.name_text.setFocus()
        else:
            self.phone_text.clear()
            self.phone_text.setFocus()

    def new_customer_registration(self):
        name = self.name_text.text()
        phone = self.phone_text.text()
        if self.validate_phone_number(phone):
            customer = self.customer_repository.create_customer(name, phone)
            self.customer_repository.set_customer(customer)
            self.name_text.setDisabled(True)
            self.phone_text.setDisabled(True)
            self.customer_confirmation_button.setEnabled(True)
            self.customer_confirmation_button.setFocus()
        else:
            self.phone_text.clear()
            self.phone_text.setFocus()

    def enable_product_ordering_section(self):
        order = self.order_repository.create_new_order(self.customer_repository.get_customer_id())
        self.order_repository.set_order(order)

    def get_order_repository(self):
        return self.order_repository

    def validate_phone_number(self, phone_number):
        # Check if the phone number is 11 digits long, starts with 0, and contains only digits
        if len(phone_number) == 11 and phone_number.startswith('0') and phone_number.isdigit():
            return True
        else:
            return False
