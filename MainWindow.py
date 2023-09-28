import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from GUI.OrderRegistrationWindow import OrderRegistrationWindow
from GUI.EditProductSpecification import EditProductSpecification
from GUI.InsertNewProduct import InsertNewProduct
from Repositories.ProductRepository import ProductRepository
import configparser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_order_window = None
        self.edit_product_window = None
        self.insert_product_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)
        main_layout = QVBoxLayout()

        new_order_button = QPushButton("New Order Registration")
        new_order_button.setFixedSize(200, 22)
        new_order_button.clicked.connect(self.open_new_order_window)
        main_layout.addWidget(new_order_button)

        edit_product_button = QPushButton("Edit Product Specification")
        edit_product_button.setFixedSize(200, 22)
        edit_product_button.clicked.connect(self.open_edit_product_window)
        main_layout.addWidget(edit_product_button)

        insert_product = QPushButton("Insert New Product")
        insert_product.setFixedSize(200, 22)
        insert_product.clicked.connect(self.open_insert_new_product_window)
        main_layout.addWidget(insert_product)

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


if __name__ == '__main__':

    if False:
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
