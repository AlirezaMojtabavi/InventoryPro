from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QVBoxLayout, QFrame, QSpacerItem, \
    QSizePolicy, QGroupBox, QFormLayout
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QFormLayout
from Repositories.OrderRepository import OrderRepository
from jdatetime import datetime as jdatetime


class OrderInformationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_order_button = None
        self.total_price_text = None
        self.current_date = None
        self.customer_number_text = None
        self.customer_name_text = None
        self.order_code_text = None
        self.order_repo = OrderRepository()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        order_group_box = QGroupBox("Order Specification")
        order_form_layout = QFormLayout()

        code_label = QLabel("Order's Code:")
        self.order_code_text = QLineEdit()
        self.order_code_text.setFixedSize(70, 22)
        self.order_code_text.returnPressed.connect(self.check_order_code)
        order_form_layout.addRow(code_label, self.order_code_text)

        customer_name_label = QLabel("Customer's Name:")
        self.customer_name_text = QLineEdit()
        self.customer_name_text.setFixedSize(170, 22)
        self.customer_name_text.setDisabled(True)
        order_form_layout.addRow(customer_name_label, self.customer_name_text)

        customer_phone_label = QLabel("Customer's phone:")
        self.customer_number_text = QLineEdit()
        self.customer_number_text.setFixedSize(100, 22)
        self.customer_number_text.setDisabled(True)
        order_form_layout.addRow(customer_phone_label, self.customer_number_text)

        current_date_label = QLabel("Date:")
        self.current_date = QLineEdit()
        self.current_date.setFixedSize(100, 22)
        self.current_date.setDisabled(True)
        order_form_layout.addRow(current_date_label, self.current_date)

        total_price_label = QLabel("Total Price:")
        self.total_price_text = QLineEdit()
        self.total_price_text.setFixedSize(100, 22)
        self.total_price_text.setDisabled(True)
        order_form_layout.addRow(total_price_label, self.total_price_text)

        self.confirm_order_button = QPushButton("Confirm")
        self.confirm_order_button.setFixedSize(70, 22)
        self.confirm_order_button.clicked.connect(self.confirm_order)
        self.confirm_order_button.setEnabled(False)
        order_form_layout.addRow(self.confirm_order_button)

        order_group_box.setLayout(order_form_layout)
        layout.addWidget(order_group_box)
        self.setLayout(layout)

    def check_order_code(self):
        order_code = self.order_code_text.text()
        order = self.order_repo.check_order_id(order_code)
        if order:
            self.customer_name_text.setText(self.order_repo.get_cutomer_name())
            self.customer_name_text.setDisabled(True)
            self.customer_number_text.setText(self.order_repo.get_custoemr_phone())
            self.customer_number_text.setDisabled(True)
            self.total_price_text.setText("{:,.0f}".format(self.order_repo.get_total_price()))
            self.total_price_text.setDisabled(True)
            jdate = jdatetime.fromgregorian(datetime=order.order_time)
            self.current_date.setText(str(jdate.strftime("%Y-%m-%d")))
            self.current_date.setDisabled(True)
            self.confirm_order_button.setEnabled(True)
            self.confirm_order_button.setFocus()
        else:
            self.order_code_text.clear()
            self.order_code_text.setFocus()

    def confirm_order(self):
        self.order_code_text.setDisabled(True)
        self.confirm_order_button.setDisabled(True)

    def get_order_repo(self):
        return self.order_repo




