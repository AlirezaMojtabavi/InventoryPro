import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, \
    QMenu, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint
from Repositories.ProductRepository import ProductRepository
from Repositories.OrderRepository import OrderRepository
from GUI.RelatedProductsWindow import RelatedProductsWindow
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class ProductsOrderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.context_menu = None
        self.layout = QVBoxLayout()
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()
        self.related_products_window = None
        self.order_table = None
        self.choose_button = None
        self.initUI()
        self.order_update_signal = OrderUpdateSignal()
        self.order_update_signal.order_updated.connect(self.update_order_rows)

    def initUI(self):
        product_ordering_label = QLabel("Product Ordering Section")
        self.layout.addWidget(product_ordering_label)
        self.prepare_order_table()

        self.choose_button = QPushButton("Choose the category", self)
        self.choose_button.setFixedSize(120, 22)
        self.choose_button.clicked.connect(self.showContextMenu)
        self.layout.addWidget(self.choose_button, alignment=Qt.AlignHCenter)

        self.finalization()
        self.setLayout(self.layout)

    def prepare_order_table(self):
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["Code", "Product Name", "Quantity", "Price"])

        font = QFont()
        font.setBold(True)

        header = self.order_table.horizontalHeader()
        for i in range(self.order_table.columnCount()):
            header.setFont(font)
            header.setDefaultAlignment(Qt.AlignCenter)

        self.order_table.setStyleSheet(
            "QTableWidget { background-color: #ffffff; border: none; }"
            "QTableWidget::item { padding: 5px; }"
            "QTableWidget::item:selected { background-color: #c0c0c0; }"
            "QTableWidget::item:alternate { background-color: #f0f0f0; }"
        )
        self.order_table.setAlternatingRowColors(True)

        self.order_table.verticalHeader().setVisible(False)
        self.order_table.resizeColumnsToContents()
        self.order_table.setColumnWidth(0, 100)
        self.order_table.setColumnWidth(1, 300)
        self.order_table.setColumnWidth(3, 80)

        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setSelectionMode(QTableWidget.SingleSelection)
        self.order_table.setSelectionBehavior(QTableWidget.SelectRows)
        # self.order_table.horizontalHeader().setStretchLastSection(True)
        self.order_table.setSortingEnabled(True)
        self.layout.addWidget(self.order_table)

    def finalization(self):
        finalize_button = QPushButton("Finalize Order")
        finalize_button.setFixedSize(120, 22)
        self.layout.addWidget(finalize_button, alignment=Qt.AlignHCenter)
        # finalize_button.setStyleSheet(
        #     "QPushButton { background-color: #ff0000; color: #ffffff; }"
        #     "QPushButton:hover { background-color: #ff3333; }"
        # )
        finalize_button.clicked.connect(self.create_sales_invoice)
        self.layout.addWidget(finalize_button)

    def showContextMenu(self, pos):
        categories_list = self.product_repository.get_all_categories()
        self.context_menu = QMenu(self)

        for categoryItem in categories_list:
            action = QAction(categoryItem.name, self)
            children = self.product_repository.get_children_label(categoryItem)
            if children:
                child_menu = QMenu(categoryItem.name, self)
                for child in children:
                    child_action = QAction(child.value, self)
                    child_action.triggered.connect(
                        lambda _, cat=categoryItem.name, ch=child.value: self.show_sub_label_products(cat, ch))
                    child_menu.addAction(child_action)
                action.setMenu(child_menu)
                self.context_menu.addAction(action)
            else:
                action.triggered.connect(self.show_related_products)
                self.context_menu.addAction(action)

        self.context_menu.popup(
            self.mapToGlobal(QPoint(self.choose_button.x(), self.choose_button.y() + self.choose_button.height())))

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
        self.related_products_window = RelatedProductsWindow(products)
        self.related_products_window.set_order_repository(self.order_repository)
        self.related_products_window.order_updated.connect(self.order_update_signal.order_updated.emit)
        self.related_products_window.show()

    def show_sub_label_products(self, category_name, child_label):
        products = self.product_repository.get_products_by_sub_label(category_name, child_label)
        self.related_products_window = RelatedProductsWindow(products)
        self.related_products_window.set_order_repository(self.order_repository)
        self.related_products_window.order_updated.connect(self.order_update_signal.order_updated.emit)
        self.related_products_window.show()

    def set_order_repository(self, order_repository):
        self.order_repository = order_repository

    def update_order_rows(self):
        order = self.order_repository.get_order()
        buffer = io.BytesIO()
        if order:
            rows = order.rows
            self.order_table.setRowCount(len(rows))

            for i, row in enumerate(rows):
                product_code = self.product_repository.get_product_by_id(row.product_id).code
                product_name = self.product_repository.get_product_by_id(row.product_id).name
                product_code = QTableWidgetItem(product_code)
                product_name = QTableWidgetItem(product_name)
                quantity_item = QTableWidgetItem(str(row.quantity))
                price_item = QTableWidgetItem(str(row.rowPrice))

                product_code.setTextAlignment(Qt.AlignCenter)
                product_name.setTextAlignment(Qt.AlignCenter)
                quantity_item.setTextAlignment(Qt.AlignCenter)
                price_item.setTextAlignment(Qt.AlignCenter)

                self.order_table.setItem(i, 0, product_code)
                self.order_table.setItem(i, 1, product_name)
                self.order_table.setItem(i, 2, quantity_item)
                self.order_table.setItem(i, 3, price_item)

    def create_sales_invoice(self):
        the_order = self.order_repository.get_order()
        buffer = io.BytesIO()
        # Create a new PDF document
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Set up the invoice layout
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 750, "Sales Invoice")
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, 700, "Order Number:")
        pdf.drawString(200, 700, str(the_order.id))

        # Add order details
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 650, "Customer Name:")
        pdf.drawString(200, 650, the_order.customer.name)
        pdf.drawString(50, 625, "Date:")
        pdf.drawString(200, 625, str(the_order.order_time))

        # Add order items
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, 575, "Code")
        pdf.drawString(100, 575, "Product")
        pdf.drawString(320, 575, "Quantity")
        pdf.drawString(400, 575, "Price")
        pdf.setFont("Helvetica", 12)

        y = 550  # Initial y-position for the first order item
        for row in the_order.rows:
            pdf.drawString(50, y, row.product.code)
            pdf.drawString(100, y, row.product.name)
            pdf.drawString(320, y, str(row.quantity))
            pdf.drawString(400, y, str(row.rowPrice))
            y -= 25  # Move to the next line

        # Add total amount
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y - 25, "Total:")
        pdf.drawString(150, y - 25, str(the_order.totalPrice))
        # Move the buffer's file pointer to the beginning
        pdf.save()

        # Save the PDF to a file
        with open("sales_invoice.pdf", "wb") as file:
            file.write(buffer.getvalue())

        # Open the PDF file in a new window
        subprocess.Popen(["start", "sales_invoice.pdf"], shell=True)