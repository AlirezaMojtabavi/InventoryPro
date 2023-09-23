import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, \
    QMenu, QAction
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QPoint

from Repositories.ProductRepository import ProductRepository
from GUI.RelatedProductsWindow import RelatedProductsWindow
from GUI.PackBoxRelatedProducts import PackBoxRelatedProducts
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
import subprocess
import reportlab.rl_config
from jdatetime import datetime as jdatetime
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class EnableFinalizeButtonSignal(QObject):
    enable_finalization = pyqtSignal()


class PackBoxStringSignal(QObject):
    enable_packBox_string = pyqtSignal()


class ProductsOrderingWidget(QWidget):
    def __init__(self, order_repo):
        super().__init__()
        self.product_ordering_group_box = None
        self.context_menu = None
        self.layout = QVBoxLayout()
        self.product_repository = ProductRepository()
        self.order_repo = order_repo
        self.related_products_window = None
        self.PackBox_Related_Products = None
        self.order_table = None
        self.choose_button = None
        self.finalize_button = None
        self.pdf = None
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
        self.order_table.setSortingEnabled(True)
        self.layout.addWidget(self.order_table)

    def enable_finalization(self):
        if self.order_repo.order_is_empty():
            self.finalize_button.setDisabled(True)
        else:
            self.finalize_button.setDisabled(False)

    def finalization(self):
        self.finalize_button = QPushButton("Finalize Order")
        self.finalize_button.setFixedSize(120, 22)
        self.finalize_button.setDisabled(True)
        self.layout.addWidget(self.finalize_button, alignment=Qt.AlignHCenter)

        self.finalize_button.clicked.connect(self.create_standard_invoice)
        self.layout.addWidget(self.finalize_button)

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
        self.related_products_window = RelatedProductsWindow(products, self.order_repo)
        # self.related_products_window.set_order_repository(self.order_repository)
        self.related_products_window.order_updated.connect(self.order_update_signal.order_updated.emit)
        self.related_products_window.enable_finalization.connect(
            self.enable_finalization_signal.enable_finalization.emit)
        self.related_products_window.show()

    def show_sub_label_products(self, category_name, child_label):
        products = self.product_repository.get_products_by_sub_label(category_name, child_label)

        if category_name == "Heets" or category_name == "Terea":
            self.PackBox_Related_Products = PackBoxRelatedProducts(products, self.order_repo, category_name)
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
        buffer = io.BytesIO()
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

    def remove_row(self, row_id):
        remove_button = self.sender()
        row_id = remove_button.property("row_id")
        if row_id is not None:
            self.order_table.removeRow(self.order_table.indexAt(remove_button.pos()).row())
            self.order_repo.remove_row(row_id)

    def create_standard_invoice(self):
        the_order = self.order_repo.get_order()
        buffer = io.BytesIO()
        self.pdf = canvas.Canvas(buffer, pagesize=A5)

        farsi_font_path = "F://InventoryManagement//Resources//B Nazanin.ttf"
        pdfmetrics.registerFont(TTFont("FarsiFont", farsi_font_path))
        Arial_font_path = "F://InventoryManagement//Resources//arial.ttf"
        pdfmetrics.registerFont(TTFont("ArialFont", Arial_font_path))
        reportlab.rl_config.canvas_basefontname = "ArialFont"

        karen_image_path = "F://InventoryManagement//Resources//logo.png"
        self.pdf.drawImage(karen_image_path, 100, 560, 200, 25)

        # __________________Part1______________________
        self.pdf.setFont("FarsiFont", 14)

        customer_name = self.convert_to_farsi("نام مشتری:")
        self.pdf.drawRightString(380, 520, customer_name)
        farsi_name = the_order.customer.name
        farsi_name_display = self.convert_to_farsi(farsi_name)
        self.pdf.drawRightString(325, 520, farsi_name_display)

        mobile_string = self.convert_to_farsi("موبایل:")
        self.pdf.drawRightString(380, 495, mobile_string)
        customer_mobile = the_order.customer.phone
        customer_mobile_display = self.convert_to_farsi(customer_mobile)
        self.pdf.drawRightString(325, 495, customer_mobile_display)

        order_number = self.convert_to_farsi("شماره سفارش:")
        self.pdf.drawRightString(170, 520, order_number)
        self.pdf.drawString(65, 520, str(the_order.id))

        date_string = self.convert_to_farsi("تاریخ:")
        self.pdf.drawRightString(170, 495, date_string)
        jdate = jdatetime.fromgregorian(datetime=the_order.order_time)
        self.pdf.drawRightString(125, 495, str(jdate.strftime("%Y-%m-%d")))

        # _________________Part2______________________

        table = self.prepare_pdf_order_table(the_order)
        table.wrapOn(self.pdf, 0, 0)
        w = (420 - table._width) / 2
        table_height = table._height
        available_height = 460
        starting_y = available_height - table_height
        table.drawOn(self.pdf, w, starting_y)

        self.pdf.setFont("Helvetica-Bold", 12)

        total_y = available_height - table_height - 20
        padding = 5

        total_text_width = self.pdf.stringWidth("Total:", "Helvetica", 12)
        price_text_width = self.pdf.stringWidth(str(the_order.totalPrice), "Helvetica", 12)

        # Calculate the width of the border based on the content width
        border_width = total_text_width + price_text_width + (3 * padding)

        # Draw the border
        self.pdf.rect(260 - padding, total_y - padding, border_width, 10 + (2 * padding))

        # Add the "Total:" text and the price
        self.pdf.drawString(260, total_y, "Total:")
        self.pdf.drawString(260 + total_text_width + 5, total_y, "{:,.0f}".format(the_order.totalPrice))

        # ___________________Part3_______________
        self.pdf.setFont("FarsiFont", 11)
        # price_unit_string = "تمامی مبالغ به ریال میباشد."
        # unit_text = self.convert_to_farsi(price_unit_string)
        # self.pdf.drawRightString(380, total_y - 35, unit_text)
        if self.packBox_invoice:
            packBox_string = "10 عدد پاکت، معادل است با 1 جعبه"
            packBox_text = self.convert_to_farsi(packBox_string)
            self.pdf.drawRightString(380, total_y - 35, packBox_text)
            payment_text_string = "لطفا پس از پرداخت، فیش واریزی را ارسال نمایید."
            payment_text = self.convert_to_farsi(payment_text_string)
            self.pdf.drawRightString(380, total_y - 50, payment_text)
        else:
            payment_text_string = "لطفا پس از پرداخت، فیش واریزی را ارسال نمایید."
            payment_text = self.convert_to_farsi(payment_text_string)
            self.pdf.drawRightString(380, total_y - 40, payment_text)


        self.pdf.setFont("FarsiFont", 8)
        karen_text_string = "مجموعه کارن آیکوس، تخصصی ترین مجموعه در حوضه محصولات آیکوس، هیتس و تریا"
        karen_text = self.convert_to_farsi(karen_text_string)
        self.pdf.drawRightString(380, 15, karen_text)

        footer_image = "F://InventoryManagement//Resources//footer.png"
        self.pdf.drawImage(footer_image, 10, 10, 130, 80)

        self.pdf.save()

        # Save the PDF to a file
        file_name = "sales_invoice" + str(the_order.id) + ".pdf"
        output_dir = "F://InventoryManagement//Output//"
        with open(output_dir + file_name, "wb") as file:
            file.write(buffer.getvalue())

        # Open the PDF file in a new window
        subprocess.Popen(["start", output_dir + file_name], shell=True)

    def convert_to_farsi(self, text):
        reshaped_name = arabic_reshaper.reshape(text)
        farsi_name_display = get_display(reshaped_name)
        return farsi_name_display

    def prepare_pdf_order_table(self, the_order):
        table_data = [["Code", "Product", "Quantity", "Price\n(Rials)"]]
        for row in the_order.rows:
            table_data.append([
                row.product.code,
                row.product.name,
                str(row.quantity),
                "{:,.0f}".format(row.rowPrice)
            ])
        table_style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])
        table = Table(table_data)
        table.setStyle(table_style)
        return table

    def enable_packBox_string(self):
        self.packBox_invoice = True
