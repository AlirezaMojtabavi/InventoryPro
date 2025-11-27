import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from GUI.OrderRegistrationWindow import OrderRegistrationWindow
from GUI.EditProductSpecification import EditProductSpecification
from GUI.EditCustomerSpecification import EditCustomerSpecification
from GUI.InsertNewProduct import InsertNewProduct
from GUI.Report.ReportWindow import ReportWindow
from PyQt5.QtGui import QIcon, QFont
from GUI.EditOrder.EditOrderWindow import EditOrderWindow
from PyQt5.QtCore import QSize, Qt
from GUI.Styles import MAIN_BUTTON_STYLE, MAIN_FONT, MAIN_BUTTON_SIZE, MAIN_BG_COLOR
from Setting import settings


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_order_window = None
        self.edit_product_window = None
        self.insert_product_window = None
        self.edit_customer_window = None
        self.edit_order_window = None
        self.report_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet(f"background-color: {MAIN_BG_COLOR};")
        self.setWindowIcon(QIcon(str(settings.ICON_PATH)))

        main_layout = QVBoxLayout()

        def make_button(text: str, slot) -> QPushButton:
            btn = QPushButton(text)
            btn.setFixedSize(*MAIN_BUTTON_SIZE)
            btn.setFont(MAIN_FONT)
            btn.setStyleSheet(MAIN_BUTTON_STYLE)
            btn.setIconSize(QSize(20, 20))
            btn.clicked.connect(slot)
            main_layout.addWidget(btn, alignment=Qt.AlignCenter)
            return btn

        make_button("New Order Registration", self.open_new_order_window)
        make_button("Edit Product", self.open_edit_product_window)
        make_button("Edit Customer", self.open_edit_customer_window)
        make_button("Insert New Product", self.open_insert_new_product_window)
        make_button("Edit Order", self.open_edit_order_window)
        make_button("Report", self.open_report_window)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def open_new_order_window(self):
        self.new_order_window = OrderRegistrationWindow()
        self.new_order_window.show()

    def open_edit_product_window(self):
        self.edit_product_window = EditProductSpecification()
        self.edit_product_window.show()

    def open_insert_new_product_window(self):
        self.insert_product_window = InsertNewProduct()
        self.insert_product_window.show()

    def open_edit_customer_window(self):
        self.edit_customer_window = EditCustomerSpecification()
        self.edit_customer_window.show()

    def open_edit_order_window(self):
        self.edit_order_window = EditOrderWindow()
        self.edit_order_window.show()

    def open_report_window(self):
        self.report_window = ReportWindow()
        self.report_window.show()


if __name__ == '__main__':

    if False:
        import pandas as pd

        # ------------------- To initialize the table of Product--------------------
        # Read the Excel file
        df = pd.read_excel('F://InventoryManagement//Resources//Product specifications.xlsx')
        product_names = df.iloc[:, 0].tolist()
        product_codes = df.iloc[:, 1].tolist()
        labels = df.iloc[:, 2].tolist()
        prices = df.iloc[:, 3].tolist()
        product_repository = ProductRepository()
        product_repository.insert_items(product_names, product_codes, labels, prices)

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
