from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QGroupBox, QFormLayout, QMenu, QAction, QComboBox
from GUI.CustomerRegistrationWidget import CustomerRegistrationWidget
from Repositories.ProductRepository import ProductRepository
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint


class InsertNewProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.confirm_button = None
        self.choose_combobox = None
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

        self.choose_combobox = QComboBox(self)
        self.choose_combobox.setFixedSize(200, 22)
        self.choose_combobox.setDisabled(True)
        self.choose_combobox.addItem("Choose a category", None)
        product_form_layout.addRow(QLabel("Category:"), self.choose_combobox)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFixedSize(70, 22)
        self.confirm_button.clicked.connect(self.confirm_product)
        self.confirm_button.setEnabled(False)
        product_form_layout.addRow(self.confirm_button)

        product_group_box.setLayout(product_form_layout)
        layout.addWidget(product_group_box)
        self.setLayout(layout)

        self.populateComboBox()
        self.choose_combobox.currentIndexChanged.connect(self.comboBoxItemChanged)

    def populateComboBox(self):
        categories_list = self.product_repo.get_all_categories()

        for categoryItem in categories_list:
            self.choose_combobox.addItem(categoryItem.name, categoryItem.name)

    def comboBoxItemChanged(self, index):
        selected_category = self.choose_combobox.itemData(index)
        if selected_category:
            self.setButtonValue(selected_category)
            self.confirm_button.setDisabled(False)
        if self.choose_combobox.currentText() == "Choose a category":
            self.confirm_button.setDisabled(True)

    def setButtonValue(self, value):
        self.choose_combobox.setCurrentText(value)

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
        self.choose_combobox.setDisabled(False)
        self.choose_combobox.setFocus()

    def enable_confirm_button(self):
        self.confirm_button.setDisabled(False)

    def confirm_product(self):
        code = self.product_code_text.text()
        name = self.product_name_text.text()
        price = float(self.price_text.text())
        category = self.choose_combobox.currentText()
        self.product_repo.insert_item(name, code, category, price)
        self.close()

