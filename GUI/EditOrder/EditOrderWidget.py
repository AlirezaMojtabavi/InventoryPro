import io
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, \
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

import configparser


class OrderUpdateSignal(QObject):
    order_updated = pyqtSignal()


class EnableFinalizeButtonSignal(QObject):
    enable_finalization = pyqtSignal()


class PackBoxStringSignal(QObject):
    enable_packBox_string = pyqtSignal()


class EditOrderWidget(QWidget):
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
        self.discounted_price = None
        self.pdf = None
        self.packBox_invoice = False
        self.initUI()
        self.order_update_signal = OrderUpdateSignal()
        self.enable_finalization_signal = EnableFinalizeButtonSignal()
        self.enable_packBox_string_signal = PackBoxStringSignal()

        # self.order_update_signal.order_updated.connect(self.update_order_rows)
        # self.enable_finalization_signal.enable_finalization.connect(self.enable_finalization)
        # self.enable_packBox_string_signal.enable_packBox_string.connect(self.enable_packBox_string)

    def initUI(self):
        self.product_ordering_group_box = QGroupBox("Product Ordering")
        self.prepare_order_table()

        self.choose_button = QPushButton("Choose the category", self)
        self.choose_button.setFixedSize(120, 22)
        # self.choose_button.clicked.connect(self.showContextMenu)
        self.layout.addWidget(self.choose_button, alignment=Qt.AlignHCenter)

        # self.finalization()
        self.product_ordering_group_box.setLayout(self.layout)
        self.layout.addWidget(self.product_ordering_group_box)
        self.setLayout(self.layout)

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
