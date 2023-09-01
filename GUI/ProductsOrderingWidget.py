import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QObject, pyqtSignal
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
        self.product_repository = ProductRepository()
        self.order_repository = OrderRepository()
        self.related_products_window = None
        self.order_table = None
        self.initUI()
        self.order_update_signal = OrderUpdateSignal()
        self.order_update_signal.order_updated.connect(self.update_order_rows)

    def initUI(self):
        layout = QVBoxLayout()
        # Product Ordering Section
        product_ordering_label = QLabel("Product Ordering Section")
        layout.addWidget(product_ordering_label)

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["Code", "Product Name", "Quantity", "Price"])

        self.order_table.setStyleSheet(
            "QTableWidget { background-color: #ffffff; border: none; }"
            "QTableWidget::item { padding: 5px; }"
            "QTableWidget::item:selected { background-color: #c0c0c0; }"
        )
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setSelectionMode(QTableWidget.SingleSelection)
        self.order_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.order_table.setAlternatingRowColors(True)
        self.order_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.order_table)

        categories_list = self.product_repository.get_all_categories()
        for categoryItem in categories_list:
            category_name = categoryItem.name
            button = QPushButton(category_name)
            button.clicked.connect(lambda checked, name=category_name: self.show_products_of_label(name))
            layout.addWidget(button)

        # Finalize Order Button
        finalize_button = QPushButton("Finalize Order")
        # finalize_button.setStyleSheet(
        #     "QPushButton { background-color: #ff0000; color: #ffffff; }"
        #     "QPushButton:hover { background-color: #ff3333; }"
        # )
        finalize_button.clicked.connect(self.create_sales_invoice)
        layout.addWidget(finalize_button)

        self.setLayout(layout)

    def show_products_of_label(self, name):
        products = self.product_repository.get_products_by_label(name)
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
