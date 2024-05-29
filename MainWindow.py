import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from GUI.OrderRegistrationWindow import OrderRegistrationWindow
from GUI.EditProductSpecification import EditProductSpecification
from GUI.EditCustomerSpecification import EditCustomerSpecification
from GUI.InsertNewProduct import InsertNewProduct
from PyQt5.QtGui import QIcon, QFont
from GUI.EditOrder.EditOrderWindow import EditOrderWindow
from PyQt5.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_order_window = None
        self.edit_product_window = None
        self.insert_product_window = None
        self.edit_customer_window = None
        self.edit_order_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setWindowIcon(QIcon('Resources\iqos-farsi-Karen-B.png'))

        main_layout = QVBoxLayout()

        button_style = """
        QPushButton {
            background-color: black;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """
        font = QFont("Arial", 12, QFont.Bold)

        new_order_button = QPushButton("New Order Registration")
        new_order_button.setFixedSize(250, 40)
        new_order_button.setFont(font)
        new_order_button.setStyleSheet(button_style)
        # new_order_button.setIcon(QIcon('path_to_icon/new_order.png'))
        new_order_button.setIconSize(QSize(20, 20))
        new_order_button.clicked.connect(self.open_new_order_window)
        main_layout.addWidget(new_order_button, alignment=Qt.AlignCenter)

        edit_product_button = QPushButton("Edit Product")
        edit_product_button.setFixedSize(250, 40)
        edit_product_button.setFont(font)
        edit_product_button.setStyleSheet(button_style)
        # edit_product_button.setIcon(QIcon('path_to_icon/edit_product.png'))
        edit_product_button.setIconSize(QSize(20, 20))
        edit_product_button.clicked.connect(self.open_edit_product_window)
        main_layout.addWidget(edit_product_button, alignment=Qt.AlignCenter)

        edit_customer_button = QPushButton("Edit Customer")
        edit_customer_button.setFixedSize(250, 40)
        edit_customer_button.setFont(font)
        edit_customer_button.setStyleSheet(button_style)
        # edit_customer_button.setIcon(QIcon('path_to_icon/edit_customer.png'))
        edit_customer_button.setIconSize(QSize(20, 20))
        edit_customer_button.clicked.connect(self.open_edit_customer_window)
        main_layout.addWidget(edit_customer_button, alignment=Qt.AlignCenter)

        insert_product_button = QPushButton("Insert New Product")
        insert_product_button.setFixedSize(250, 40)
        insert_product_button.setFont(font)
        insert_product_button.setStyleSheet(button_style)
        # insert_product_button.setIcon(QIcon('path_to_icon/insert_product.png'))
        insert_product_button.setIconSize(QSize(20, 20))
        insert_product_button.clicked.connect(self.open_insert_new_product_window)
        main_layout.addWidget(insert_product_button, alignment=Qt.AlignCenter)

        edit_order_button = QPushButton("ٍEdit Order")
        edit_order_button.setFixedSize(250, 40)
        edit_order_button.setFont(font)
        edit_order_button.setStyleSheet(button_style)
        # edit_order_button.setIcon(QIcon('path_to_icon/insert_product.png'))
        edit_order_button.setIconSize(QSize(20, 20))
        edit_order_button.clicked.connect(self.open_edit_order_window)
        main_layout.addWidget(edit_order_button, alignment=Qt.AlignCenter)

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
