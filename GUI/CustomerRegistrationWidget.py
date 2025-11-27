from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QVBoxLayout, QFrame, QSpacerItem, \
    QSizePolicy, QGroupBox, QFormLayout
from GUI.Styles import CUSTOMER_INPUT_STYLE, CUSTOMER_GROUPBOX_STYLE, CUSTOMER_CONFIRM_BUTTON_STYLE, CUSTOMER_LABEL_FONT
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
        customer_group_box.setStyleSheet(CUSTOMER_GROUPBOX_STYLE)
        customer_form_layout = QFormLayout()
        customer_form_layout.setContentsMargins(10, 25, 5, 15)

        phone_label = QLabel("Phone Number:")
        phone_label.setFont(CUSTOMER_LABEL_FONT)
        self.phone_text = QLineEdit()
        # self.phone_text.setFixedSize(100, 22)
        self.phone_text.setFixedSize(190, 32)
        self.phone_text.setStyleSheet(CUSTOMER_INPUT_STYLE)
        self.phone_text.returnPressed.connect(self.check_phone_number)
        customer_form_layout.addRow(phone_label, self.phone_text)

        name_label = QLabel("Name of Customer:")
        name_label.setFont(CUSTOMER_LABEL_FONT)
        self.name_text = QLineEdit()
        self.name_text.setFixedSize(260, 32)
        self.name_text.setStyleSheet(CUSTOMER_INPUT_STYLE)
        self.name_text.returnPressed.connect(self.new_customer_registration)
        customer_form_layout.addRow(name_label, self.name_text)

        self.customer_confirmation_button = QPushButton("Confirm Customer")
        self.customer_confirmation_button.setFixedSize(210, 40)
        self.customer_confirmation_button.setStyleSheet(CUSTOMER_CONFIRM_BUTTON_STYLE)
        self.customer_confirmation_button.clicked.connect(self.enable_product_ordering_section)
        self.customer_confirmation_button.setEnabled(False)
        customer_form_layout.addItem(QSpacerItem(10, 25, QSizePolicy.Minimum, QSizePolicy.Fixed))
        customer_form_layout.addRow(self.customer_confirmation_button)

        customer_group_box.setLayout(customer_form_layout)
        layout.addWidget(customer_group_box)
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
        self.customer_confirmation_button.setEnabled(False)

    def get_order_repository(self):
        return self.order_repository

    def validate_phone_number(self, phone_number):
        # Check if the phone number is 11 digits long, starts with 0, and contains only digits
        if len(phone_number) == 11 and phone_number.startswith('0') and phone_number.isdigit():
            return True
        else:
            return False
