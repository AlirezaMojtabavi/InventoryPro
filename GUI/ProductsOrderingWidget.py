from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, \
    QMenu, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint

from Repositories.ProductRepository import ProductRepository, Category, SubCat1, SubCat2, SubCat3
from GUI.RelatedProductsWindow import RelatedProductsWindow
from GUI.PackBoxRelatedProducts import PackBoxRelatedProducts
import subprocess
from Reports.InvoicePdf import InvoicePdf

from GUI.Styles import ORDER_TABLE_STYLE, ORDER_GROUPBOX_STYLE, \
    ORDER_CHOOSE_BUTTON_STYLE, ORDER_FINALIZE_BUTTON_STYLE, CATEGORY_MENU_STYLE


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class EnableFinalizeButtonSignal(QObject):
    enable_finalization = pyqtSignal()


class PackBoxStringSignal(QObject):
    enable_packBox_string = pyqtSignal()


class ProductsOrderingWidget(QWidget):
    def __init__(self, order_repo):
        super().__init__()
        self.skip_close_confirmation = False
        self.product_ordering_group_box = None
        self.context_menu = None
        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.product_repository = ProductRepository()
        self.order_repo = order_repo
        self.related_products_window = None
        self.PackBox_Related_Products = None
        self.order_table = None
        self.choose_button = None
        self.finalize_button = None
        self.discounted_price = None
        self.packBox_invoice = False
        self.initUI()
        self.order_update_signal = OrderUpdateSignal()
        self.enable_finalization_signal = EnableFinalizeButtonSignal()
        self.enable_packBox_string_signal = PackBoxStringSignal()

        self.order_update_signal.order_updated.connect(self.update_order_rows)
        self.enable_finalization_signal.enable_finalization.connect(self.enable_finalization)
        self.enable_packBox_string_signal.enable_packBox_string.connect(self.enable_packBox_string)

    def initUI(self):
        self.product_ordering_group_box = QGroupBox("Product Ordering")
        self.product_ordering_group_box.setStyleSheet(ORDER_GROUPBOX_STYLE)

        group_layout = QVBoxLayout(self.product_ordering_group_box)
        group_layout.setContentsMargins(15, 20, 15, 15)

        self.prepare_order_table()
        group_layout.addWidget(self.order_table)
        self.choose_button = QPushButton("Choose category", self)
        self.choose_button.setFixedSize(200, 40)
        self.choose_button.setStyleSheet(ORDER_CHOOSE_BUTTON_STYLE)

        self.choose_button.clicked.connect(self.showContextMenu)
        group_layout.addWidget(self.choose_button, alignment=Qt.AlignHCenter)

        self.finalization()
        self.finalize_button.setFixedSize(200, 40)
        self.finalize_button.setStyleSheet(ORDER_FINALIZE_BUTTON_STYLE)
        group_layout.addWidget(self.finalize_button, alignment=Qt.AlignHCenter)
        self.product_ordering_group_box.setLayout(self.layout())
        self.main_layout.addWidget(self.product_ordering_group_box)

    def prepare_order_table(self):
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["Code", "Product Name", "Quantity", "Price", "Actions", "Discount"])

        font = QFont()
        font.setBold(True)

        header = self.order_table.horizontalHeader()
        for i in range(self.order_table.columnCount()):
            header.setFont(font)
            header.setDefaultAlignment(Qt.AlignCenter)

        self.order_table.setStyleSheet(ORDER_TABLE_STYLE)

        self.order_table.setAlternatingRowColors(True)

        self.order_table.verticalHeader().setVisible(False)
        self.order_table.resizeColumnsToContents()
        self.order_table.setColumnWidth(0, 100)
        self.order_table.setColumnWidth(1, 300)
        self.order_table.setColumnWidth(3, 80)

        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setSelectionMode(QTableWidget.SingleSelection)
        self.order_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.order_table.setSortingEnabled(True)

    def enable_finalization(self):
        if self.order_repo.order_is_empty():
            self.finalize_button.setDisabled(True)
        else:
            self.finalize_button.setDisabled(False)

    def finalization(self):
        self.finalize_button = QPushButton("Finalize Order")
        self.finalize_button.setDisabled(True)
        self.finalize_button.clicked.connect(self.create_standard_invoice)

    def showContextMenu(self, pos):
        categories_list = self.product_repository.get_all_categories()
        self.context_menu = QMenu(self)

        menu_font = QFont()
        menu_font.setBold(True)
        menu_font.setPointSize(11)
        self.context_menu.setFont(menu_font)
        self.context_menu.setStyleSheet(CATEGORY_MENU_STYLE)

        for category in categories_list:
            action = QAction(category.value, self)

            children = self.product_repository.get_children_label(category.value)
            if children:
                child_menu = QMenu(category.value, self)
                child_menu.setFont(menu_font)
                child_menu.setStyleSheet(CATEGORY_MENU_STYLE)

                for child in children:
                    child_action = QAction(child.value, self)

                    child_action.triggered.connect(
                        lambda _, cat=category, ch=child.value: self.show_sub_label_products(cat, ch))
                    child_menu.addAction(child_action)

                action.setMenu(child_menu)
                self.context_menu.addAction(action)
            else:
                action.triggered.connect(self.show_related_products)
                self.context_menu.addAction(action)

        self.context_menu.popup(self.mapToGlobal(QPoint(self.choose_button.x(),
                                    self.choose_button.y() + self.choose_button.height())))

    def show_child_labels(self, category_name):
        action = self.sender()
        children_label = self.product_repository.get_children_label(category_name)
        submenu = QMenu(category_name.value, self)
        for child in children_label:
            child_action = QAction(child.value, self)
            child_action.triggered.connect(
                lambda _, cat=category_name.value, ch=child.value: self.show_sub_label_products(cat, ch))
            submenu.addAction(child_action)
        self.context_menu = QMenu(category_name.value, self)
        self.context_menu.addMenu(submenu)
        self.context_menu.exec_(self.mapToGlobal(action.parentWidget().pos()))

    def show_related_products(self):
        action = self.sender()
        category_name = action.text()
        products = self.product_repository.get_products_by_label(category_name)
        self.related_products_window = RelatedProductsWindow(products, self.order_repo)
        # self.related_products_window.set_order_repository(self.order_repository)
        self.related_products_window.order_updated.connect(self.order_update_signal.order_updated.emit)
        self.related_products_window.enable_finalization.connect(
            self.enable_finalization_signal.enable_finalization.emit)
        self.related_products_window.show()

    def show_sub_label_products(self, category, child_label):
        if isinstance(category, str):
            try:
                category_enum = Category[category]
            except KeyError:
                category_enum = Category(category)
        else:
            category_enum = category

        products = self.product_repository.get_products_by_sub_label(category, child_label)

        # Special case for Cat2 / Cat3
        if category_enum in (Category.Cat2, Category.Cat3):
            self.PackBox_Related_Products = PackBoxRelatedProducts(
                products,
                self.order_repo,
                category_enum.value)
            self.PackBox_Related_Products.order_updated.connect(self.order_update_signal.order_updated.emit)
            self.PackBox_Related_Products.enable_packBox.connect(
                self.enable_packBox_string_signal.enable_packBox_string.emit)
            self.PackBox_Related_Products.enable_finalization.connect(
                self.enable_finalization_signal.enable_finalization.emit)
            self.PackBox_Related_Products.show()
        else:
            self.related_products_window = RelatedProductsWindow(products, self.order_repo)
            self.related_products_window.order_updated.connect(self.order_update_signal.order_updated.emit)
            self.related_products_window.enable_finalization.connect(
                self.enable_finalization_signal.enable_finalization.emit)
            self.related_products_window.show()

    def update_order_rows(self):
        order = self.order_repo.get_order()
        if order:
            rows = order.rows
            self.order_table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                product_code = self.product_repository.get_product_by_id(row.product_id).code
                product_name = self.product_repository.get_product_by_id(row.product_id).name
                product_code = QTableWidgetItem(product_code)
                product_name = QTableWidgetItem(product_name)
                if product_code == "9999":
                    quantity_item = QTableWidgetItem(str(0))
                    delivery_fee = row.quantity * 10000
                    price_item = QTableWidgetItem("{:,.0f}".format(delivery_fee))
                else:
                    price_item = QTableWidgetItem("{:,.0f}".format(row.rowPrice))
                    quantity_item = QTableWidgetItem(str(row.quantity))

                product_code.setTextAlignment(Qt.AlignCenter)
                product_name.setTextAlignment(Qt.AlignCenter)
                quantity_item.setTextAlignment(Qt.AlignCenter)
                price_item.setTextAlignment(Qt.AlignCenter)

                self.order_table.setItem(i, 0, product_code)
                self.order_table.setItem(i, 1, product_name)
                self.order_table.setItem(i, 2, quantity_item)
                self.order_table.setItem(i, 3, price_item)

                remove_button = QPushButton("Remove", self.order_table)
                remove_button.setObjectName(f"removeButton_{i}")
                # remove_button.clicked.connect(lambda _, row_id=row.id: self.remove_row(row.id))
                remove_button.setProperty("row_id", row.id)
                remove_button.clicked.connect(self.remove_row)
                self.order_table.setCellWidget(i, 4, remove_button)
                self.order_table.setColumnWidth(4, remove_button.sizeHint().width())

                discount_button = QPushButton("Discount", self.order_table)
                discount_button.setObjectName(f"discount_{i}")
                # remove_button.clicked.connect(lambda _, row_id=row.id: self.remove_row(row.id))
                discount_button.setProperty("row_id", row.id)
                discount_button.clicked.connect(self.open_discount_window)
                self.order_table.setCellWidget(i, 5, discount_button)
                self.order_table.setColumnWidth(5, discount_button.sizeHint().width())

    def remove_row(self):
        remove_button = self.sender()
        row_id = remove_button.property("row_id")
        if row_id is not None:
            self.order_table.removeRow(self.order_table.indexAt(remove_button.pos()).row())
            self.order_repo.remove_row(row_id)

    def create_standard_invoice(self):
        the_order = self.order_repo.get_order()

        pdf_generator = InvoicePdf()
        output_path = pdf_generator.build(the_order, self.packBox_invoice)

        subprocess.Popen(["start", output_path], shell=True)
        self.skip_close_confirmation = True
        x = self.parentWidget()
        x.close()
        self.order_repo.finish()

    def enable_packBox_string(self):
        self.packBox_invoice = True

    def open_discount_window(self):
        discount_button = self.sender()
        row_id = discount_button.property("row_id")
        item_number = self.order_table.indexAt(discount_button.pos()).row()
        self.discounted_price = QLineEdit()
        self.discounted_price.returnPressed.connect(lambda: self.set_discounted_price(row_id, item_number))
        self.discounted_price.setFocus()
        self.discounted_price.show()

    def set_discounted_price(self, row_id, item_number):
        discounted_price = self.discounted_price.text()
        discounted_price = float(discounted_price)

        price_item = QTableWidgetItem("{:,.0f}".format(discounted_price))
        self.order_table.setItem(item_number, 3, price_item)
        self.order_repo.discounted_row(row_id, discounted_price)
        self.discounted_price.close()
