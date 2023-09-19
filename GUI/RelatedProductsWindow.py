from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QSpinBox, QGridLayout, QScrollArea, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class EnableFinalizeButtonSignal(QObject):
    enable_finalization = pyqtSignal()


class RelatedProductsWindow(QWidget):
    order_updated = pyqtSignal()
    enable_finalization = pyqtSignal()

    def __init__(self, products, order_repo):
        super().__init__()
        self.products = products
        self.order_repo = order_repo
        self.content_layout = None
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        self.content_layout = QGridLayout(content_widget)
        for i, productItem in enumerate(self.products):
            product_code = QLabel(productItem.code)
            product_code.setFixedSize(40, 25)
            product_name = QLabel(productItem.name)
            product_name.setFixedSize(215, 25)
            spinBox = QSpinBox()
            spinBox.setFixedSize(50, 25)
            spinBox.setMinimum(0)
            spinBox.setMaximum(999)
            if productItem.price == 0:
                spinBox.setDisabled(True)
            self.content_layout.addWidget(product_code, i, 0)
            self.content_layout.addWidget(product_name, i, 1)
            self.content_layout.addWidget(spinBox, i, 2)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_button_clicked)

        # main_layout = QGridLayout(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(confirm_button)
        self.setWindowTitle('Related Products Window')
        self.setGeometry(200, 50, 450, 600)

    # def delivery(self):
    #     product_code = QLabel(self.products.code)
    #     product_code.setFixedSize(40, 25)
    #     product_name = QLabel(self.products.name)
    #     product_name.setFixedSize(215, 25)
    #     price_text = QLineEdit()
    #     price_text.setFixedSize(50, 25)

    def confirm_button_clicked(self):
        for i in range(len(self.products)):
            spinBox = self.content_layout.itemAtPosition(i, 2).widget()
            quantity = spinBox.value()
            if quantity > 0:
                product = self.products[i]
                if product.code == "9999":
                    delivery_price = quantity * 10000
                    self.add_delivery_row(delivery_price)
                else:
                    self.add_order_row(product_id=product.id, quantity=quantity)
        self.order_updated.emit()
        self.enable_finalization.emit()
        self.close()

    # def set_order_repository(self, order_repo):
    #     self.order_repo = order_repo

    def add_order_row(self, product_id, quantity):
        self.order_repo.add_row(product_id, quantity)

    def add_delivery_row(self, price):
        self.order_repo.add_delivery_row(price)
