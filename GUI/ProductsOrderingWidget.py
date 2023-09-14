import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, \
    QMenu, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint
from psycopg2.extras import DictRow

from Repositories.ProductRepository import ProductRepository
from Repositories.OrderRepository import OrderRepository
from GUI.RelatedProductsWindow import RelatedProductsWindow
from reportlab.lib.pagesizes import letter, A4, A5
from reportlab.pdfgen import canvas
import subprocess
import reportlab.rl_config
from jdatetime import datetime as jdatetime
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from PIL import Image
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class ProductsOrderingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.product_ordering_group_box = None
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
        self.product_ordering_group_box = QGroupBox("Product Ordering")
        self.prepare_order_table()

        self.choose_button = QPushButton("Choose the category", self)
        self.choose_button.setFixedSize(120, 22)
        self.choose_button.clicked.connect(self.showContextMenu)
        self.layout.addWidget(self.choose_button, alignment=Qt.AlignHCenter)

        self.finalization()
        self.product_ordering_group_box.setLayout(self.layout)
        self.layout.addWidget(self.product_ordering_group_box)
        self.setLayout(self.layout)

    def prepare_order_table(self):
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Code", "Product Name", "Quantity", "Price", "Actions"])

        font = QFont()
        font.setBold(True)

        header = self.order_table.horizontalHeader()
        for i in range(self.order_table.columnCount()):
            header.setFont(font)
            header.setDefaultAlignment(Qt.AlignCenter)
            # header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

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
        finalize_button.clicked.connect(self.create_standard_invoice)
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

                remove_button = QPushButton("Remove", self.order_table)
                remove_button.setObjectName(f"removeButton_{i}")
                # remove_button.clicked.connect(lambda _, row_id=row.id: self.remove_row(row.id))
                remove_button.setProperty("row_id", row.id)
                remove_button.clicked.connect(self.remove_row)
                self.order_table.setCellWidget(i, 4, remove_button)
                self.order_table.setColumnWidth(4, remove_button.sizeHint().width())

    def remove_row(self, row_id):
        remove_button = self.sender()
        row_id = remove_button.property("row_id")
        if row_id is not None:
            self.order_table.removeRow(self.order_table.indexAt(remove_button.pos()).row())
            self.order_repository.remove_row(row_id)

    def create_sales_invoice(self):
        the_order = self.order_repository.get_order()
        buffer = io.BytesIO()
        # Create a new PDF document
        pdf = canvas.Canvas(buffer, pagesize=letter)
        reportlab.rl_config.canvas_basefontname = "Arial"

        pdfmetrics.registerFont(TTFont('Farsi', 'F:\InventoryManagement\B Nazanin.ttf'))

        # Set up the invoice layout
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 750, "Sales Invoice")
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, 700, "Order Number:")
        pdf.drawString(200, 700, str(the_order.id))

        # Add order details
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 650, "Customer Name:")
        pdf.saveState()
        pdf.translate(200, 650)  # Move the origin to the starting point of the text
        pdf.rotate(90)  # Rotate the canvas 90 degrees
        pdf.drawString(0, 0, the_order.customer.name, direction="rtl")
        pdf.restoreState()

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
        file_name = "sales_invoice" + str(the_order.id) + ".pdf"
        with open(file_name, "wb") as file:
            file.write(buffer.getvalue())

        # Open the PDF file in a new window
        subprocess.Popen(["start", file_name], shell=True)

    def create_sales_invoice_farsi(self):
        the_order = self.order_repository.get_order()
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A5)

        farsi_font_path = "B Nazanin.ttf"
        pdfmetrics.registerFont(TTFont("FarsiFont", farsi_font_path))

        styles = getSampleStyleSheet()
        arabic_style = ParagraphStyle("FarsiStyle", parent=styles["Normal"], fontName="FarsiFont")

        elements = []
        image_path = "logo.jpg"
        image = Image(image_path, width=200, height=30)
        elements.append(image)

        elements.append(Spacer(1, 20 * mm))

        order_number = self.convert_to_farsi("شماره سفارش:")
        pdf.drawString(50, 675, order_number)
        pdf.drawString(150, 675, str(the_order.id))

        customer_name = self.convert_to_farsi("نام مشتری:")
        pdf.drawString(50, 650, customer_name)

        farsi_name = the_order.customer.name
        farsi_name_display = self.convert_to_farsi(farsi_name)
        pdf.drawString(150, 650, farsi_name_display)

        date_string = self.convert_to_farsi("تاریخ:")
        pdf.drawString(50, 625, date_string)
        jdate = jdatetime.fromgregorian(datetime=the_order.order_time)
        pdf.drawString(150, 625, str(jdate))

        # Add the table with order rows
        elements.append(Spacer(1, 10 * mm))
        table_data = [["Code", "Product", "Quantity", "Price"]]
        for row in the_order.rows:
            table_data.append([
                row.product.code,
                row.product.name,
                str(row.quantity),
                str(row.rowPrice)
            ])
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table = Table(table_data)
        table.setStyle(table_style)
        elements.append(table)

        # Add the total price
        elements.append(Spacer(1, 10 * mm))
        total_label = self.convert_to_farsi("جمع کل:")
        pdf.drawString(50, 50, total_label)
        pdf.drawString(150, 50, str(the_order.totalPrice))
        # Build the PDF document
        pdf.build(elements)

        # Save the PDF to a file
        file_name = "sales_invoice" + str(the_order.id) + ".pdf"
        with open(file_name, "wb") as file:
            file.write(buffer.getvalue())

        # Open the PDF file
        subprocess.Popen(["start", file_name], shell=True)

    def create_standard_invoice(self):
        the_order = self.order_repository.get_order()
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A5)

        farsi_font_path = "F:\InventoryManagement\Resources\B Nazanin.ttf"
        pdfmetrics.registerFont(TTFont("FarsiFont", farsi_font_path))
        reportlab.rl_config.canvas_basefontname = "Arial"

        karen_image_path = "F:\InventoryManagement\Resources\logo.png"
        pdf.drawImage(karen_image_path, 100, 560, 200, 25)

        # __________________Part1______________________
        pdf.setFont("FarsiFont", 12)

        pdf.setFont("FarsiFont", 12)
        customer_name = self.convert_to_farsi("نام مشتری:")
        pdf.drawRightString(380, 520, customer_name)
        farsi_name = the_order.customer.name
        farsi_name_display = self.convert_to_farsi(farsi_name)
        pdf.drawRightString(325, 520, farsi_name_display)

        mobile_string = self.convert_to_farsi("شماره موبایل:")
        pdf.drawRightString(380, 495, mobile_string)
        customer_mobile = the_order.customer.phone
        customer_mobile_display = self.convert_to_farsi(customer_mobile)
        pdf.drawRightString(325, 495, customer_mobile_display)

        order_number = self.convert_to_farsi("شماره سفارش:")
        pdf.drawRightString(170, 520, order_number)
        pdf.drawString(85, 520, str(the_order.id))

        pdf.setFont("FarsiFont", 12)
        date_string = self.convert_to_farsi("تاریخ:")
        pdf.drawRightString(170, 495, date_string)
        jdate = jdatetime.fromgregorian(datetime=the_order.order_time)
        pdf.drawRightString(125, 495, str(jdate.strftime("%Y-%m-%d")))

        # _________________Part2______________________

        table, y = self.prepare_pdf_order_table(the_order)
        table.wrapOn(pdf, 0, 0)
        w = (420 - table._width) / 2
        table_height = table._height
        available_height = 440  # Adjust this value as needed
        starting_y = available_height - table_height

        table.drawOn(pdf, w, starting_y)

        # ___________________Part3_______________

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(260, available_height - table_height - 15, "Total:")
        pdf.drawString(295, available_height - table_height - 15, str(the_order.totalPrice))

        about_us_image = "F://InventoryManagement//Resources//about us.png"
        pdf.drawImage(about_us_image, 10, 10, 130, 40)

        pdf.save()

        # Save the PDF to a file
        file_name = "sales_invoice" + str(the_order.id) + ".pdf"
        # output_dir = "F://InventoryManagement//Output//"
        with open(file_name, "wb") as file:
            file.write(buffer.getvalue())

        # Open the PDF file in a new window
        subprocess.Popen(["start", file_name], shell=True)

    def convert_to_farsi(self, text):
        reshaped_name = arabic_reshaper.reshape(text)
        farsi_name_display = get_display(reshaped_name)
        return farsi_name_display

    def prepare_pdf_order_table(self, the_order):
        table_data = [["Code", "Product", "Quantity", "Price"]]
        y = 430
        for row in the_order.rows:
            table_data.append([
                row.product.code,
                row.product.name,
                str(row.quantity),
                str(row.rowPrice)
            ])
            y -= 20
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table = Table(table_data)
        table.setStyle(table_style)
        return table, y

