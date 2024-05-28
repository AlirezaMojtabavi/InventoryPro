from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QFormLayout
from GUI.CustomerRegistrationWidget import CustomerRegistrationWidget
from Repositories.ProductRepository import ProductRepository
from GUI.ProductsOrderingWidget import ProductsOrderingWidget


class InsertNewProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_button = None
        self.category_text = None
        self.price_text = None
        self.product_name_text = None
        self.product_code_text = None
        self.product_repo = ProductRepository()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        product_group_box = QGroupBox("Product Specification")
        product_form_layout = QFormLayout()

        code_label = QLabel("Product's Code:")
        self.product_code_text = QLineEdit()
        self.product_code_text.setFixedSize(70, 22)
        self.product_code_text.returnPressed.connect(self.check_product_code)
        product_form_layout.addRow(code_label, self.product_code_text)

        name_label = QLabel("Product's Name:")
        self.product_name_text = QLineEdit()
        self.product_name_text.setFixedSize(170, 22)
        self.product_name_text.setDisabled(True)
        self.product_name_text.returnPressed.connect(self.pass_product_name)
        product_form_layout.addRow(name_label, self.product_name_text)

        price_label = QLabel("New Price:")
        self.price_text = QLineEdit()
        self.price_text.setFixedSize(100, 22)
        self.price_text.returnPressed.connect(self.pass_product_price)
        self.price_text.setDisabled(True)
        product_form_layout.addRow(price_label, self.price_text)

        category_label = QLabel("Category:")
        self.category_text = QLineEdit()
        self.category_text.setFixedSize(100, 22)
        self.category_text.returnPressed.connect(self.enable_confirm_button)
        self.category_text.setDisabled(True)
        product_form_layout.addRow(category_label, self.category_text)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFixedSize(70, 22)
        self.confirm_button.clicked.connect(self.confirm_product)
        self.confirm_button.setEnabled(False)
        product_form_layout.addRow(self.confirm_button)

        product_group_box.setLayout(product_form_layout)
        layout.addWidget(product_group_box)
        self.setLayout(layout)

    def check_product_code(self):
        product_code = self.product_code_text.text()
        product = self.product_repo.get_product_by_code(product_code)
        if product:
            self.product_name_text.setText(product.name)
            self.product_name_text.setDisabled(True)
            self.price_text.setDisabled(True)
            self.product_code_text.setFocus()
        else:
            if len(product_code) == 4 and product_code.isdigit():
                self.product_name_text.setDisabled(False)
                self.product_code_text.setDisabled(True)
                self.product_name_text.setFocus()
            else:
                self.product_code_text.clear()
                self.product_code_text.setFocus()

    def pass_product_name(self):
        self.price_text.setDisabled(False)
        self.price_text.setFocus()

    def pass_product_price(self):
        self.category_text.setDisabled(False)
        self.category_text.setFocus()

    def enable_confirm_button(self):
        self.confirm_button.setDisabled(False)

    def confirm_product(self):
        code = self.product_code_text.text()
        name = self.product_name_text.text()
        price = float(self.price_text.text())
        category = self.category_text.text()
        self.product_repo.insert_item(name, code, category, price)
        self.close()
