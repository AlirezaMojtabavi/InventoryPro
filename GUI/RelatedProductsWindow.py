from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QSpinBox, QGridLayout, QScrollArea
from PyQt5.QtCore import QObject, pyqtSignal


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class RelatedProductsWindow(QWidget):
    order_updated = pyqtSignal()

    def __init__(self, products):
        super().__init__()
        self.products = products
        self.order_repository = None
        self.content_layout = None
        self.initUI()

    def initUI(self):
        content_widget = QWidget()
        self.content_layout = QGridLayout(content_widget)
        for i, productItem in enumerate(self.products):
            label = QLabel(productItem.name)
            spinBox = QSpinBox()
            self.content_layout.addWidget(label, i, 0)
            self.content_layout.addWidget(spinBox, i, 1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        confirm_button = QPushButton("Confirm")
        # button.clicked.connect(self.show_product_of_label)
        confirm_button.clicked.connect(self.confirm_button_clicked)

        main_layout = QGridLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(confirm_button)
        self.setWindowTitle('Related Products Window')
        self.setGeometry(200, 50, 400, 600)
        # self.ProductsSection = ProductsSection()
        # self.product_ordering_widget.hide()
        # self.layout.addWidget(self.product_ordering_widget)
        #
        # self.setLayout(self.layout)

    def confirm_button_clicked(self):
        for i in range(len(self.products)):
            spinBox = self.content_layout.itemAtPosition(i, 1).widget()
            quantity = spinBox.value()
            if quantity > 0:
                product = self.products[i]
                self.add_order_row(product_id=product.id, quantity=quantity)
        self.order_updated.emit()
        self.close()

    def set_order_repository(self, order_repo):
        self.order_repository = order_repo

    def add_order_row(self, product_id, quantity):
        self.order_repository.add_row(product_id, quantity)
