from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QSpinBox, QGridLayout, QScrollArea, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class EnableFinalizeButtonSignal(QObject):
    enable_finalization = pyqtSignal()


class PackBoxRelatedProducts(QWidget):
    order_updated = pyqtSignal()
    enable_finalization = pyqtSignal()

    def __init__(self, products, order_repo, category_name):
        super().__init__()
        self.products = products
        self.order_repo = order_repo
        self.category_name = category_name
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

            pack_spinBox = QSpinBox()
            pack_spinBox.setFixedSize(50, 25)
            pack_spinBox.setMinimum(0)
            pack_spinBox.setMaximum(999)
            box_spinBox = QSpinBox()
            box_spinBox.setFixedSize(50, 25)
            box_spinBox.setMinimum(0)
            box_spinBox.setMaximum(999)
            if productItem.price == 0:
                pack_spinBox.setDisabled(True)
                box_spinBox.setDisabled(True)

            self.content_layout.addWidget(product_code, i, 0)
            self.content_layout.addWidget(product_name, i, 1)
            self.content_layout.addWidget(box_spinBox, i, 2)
            self.content_layout.addWidget(pack_spinBox, i, 3)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_button_pack_box_clicked)

        # main_layout = QGridLayout(self)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(confirm_button)
        self.setWindowTitle('Related Products Window')
        self.setGeometry(200, 50, 450, 600)

    def confirm_button_pack_box_clicked(self):
        for i in range(len(self.products)):
            box_spinBox = self.content_layout.itemAtPosition(i, 2).widget()
            pack_spinBox = self.content_layout.itemAtPosition(i, 3).widget()
            box_quantity = box_spinBox.value()
            pack_quantity = pack_spinBox.value()
            if box_quantity > 0 or pack_quantity > 0:
                product = self.products[i]
                if (box_quantity > 0) and not(pack_quantity > 0):
                    self.add_order_row(product_id=product.id, quantity=box_quantity * 10)
                elif (pack_quantity > 0) and not(box_quantity > 0):
                    self.add_order_row(product_id=product.id, quantity=pack_quantity)
                elif (box_quantity > 0) and (pack_quantity > 0):
                    self.add_order_row(product_id=product.id, quantity=pack_quantity + box_quantity * 10)

        self.order_updated.emit()
        self.enable_finalization.emit()
        self.close()

    def add_order_row(self, product_id, quantity):
        self.order_repo.add_row(product_id, quantity)

    def add_delivery_row(self, price):
        self.order_repo.add_delivery_row(price)
