from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QFormLayout
from Repositories.CustomerRepository import CustomerRepository


class EditCustomerSpecification(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_button = None
        self.customer_name_text = None
        self.phone_number_text = None
        self.customer_repo = CustomerRepository()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        customer_group_box = QGroupBox("Customer Specification")
        customer_form_layout = QFormLayout()
        self.customer_name_text = QLineEdit()
        self.customer_name_text.setDisabled(True)

        phone_number_label = QLabel("Phone Number:")
        self.phone_number_text = QLineEdit()
        self.phone_number_text.setFixedSize(90, 22)
        self.phone_number_text.returnPressed.connect(self.check_phone_number)
        customer_form_layout.addRow(phone_number_label, self.phone_number_text)

        name_label = QLabel("Customer's Name:")
        self.customer_name_text.setFixedSize(150, 22)
        self.customer_name_text.returnPressed.connect(self.name_modified)
        customer_form_layout.addRow(name_label, self.customer_name_text)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFixedSize(70, 22)
        self.confirm_button.clicked.connect(self.confirm)
        self.confirm_button.setEnabled(False)
        customer_form_layout.addRow(self.confirm_button)

        customer_group_box.setLayout(customer_form_layout)
        layout.addWidget(customer_group_box)
        self.setLayout(layout)

    def check_phone_number(self):
        phone_number = self.phone_number_text.text()
        if self.validate_phone_number(phone_number):
            if self.customer_repo.check_phone_number(phone_number):
                customer = self.customer_repo.get_customer_by_phone(phone_number)
                self.customer_repo.set_customer(customer)
                name = self.customer_repo.get_customer_name()
                self.customer_name_text.setEnabled(True)
                self.customer_name_text.setText(name)
                self.customer_name_text.setFocus()
                # self.customer_name_text.setDisabled(True)
                # self.phone_number_text.setDisabled(True)
                # self.confirm_button.setEnabled(True)
                # self.confirm_button.setFocus()
            else:
                self.phone_number_text.clear()
                self.customer_name_text.clear()
                self.phone_number_text.setFocus()
        else:
            self.phone_number_text.clear()
            self.customer_name_text.clear()
            self.phone_number_text.setFocus()

    def validate_phone_number(self, phone_number):
        # Check if the phone number is 11 digits long, starts with 0, and contains only digits
        if len(phone_number) == 11 and phone_number.startswith('0') and phone_number.isdigit():
            return True
        else:
            return False

    def name_modified(self):
        self.customer_name_text.setEnabled(False)
        self.phone_number_text.setEnabled(False)
        self.confirm_button.setEnabled(True)

    def confirm(self):
        customer_name = self.customer_name_text.text()
        phone_number = self.phone_number_text.text()
        self.customer_repo.edit_customer(phone_number, customer_name)
        self.close()
