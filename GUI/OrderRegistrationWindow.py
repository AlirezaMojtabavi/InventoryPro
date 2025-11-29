from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from GUI.CustomerRegistrationWidget import CustomerRegistrationWidget
from GUI.ProductsOrderingWidget import ProductsOrderingWidget


class OrderRegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.customer_registration_widget = None
        self.product_ordering_widget = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.customer_registration_widget = CustomerRegistrationWidget()
        self.customer_registration_widget.customer_confirmation_button.clicked.connect(
            self.retrieve_order)
        layout.addWidget(self.customer_registration_widget)
        self.setLayout(layout)
        self.setWindowTitle('Customer Registration Window')
        self.setGeometry(100, 60, 600, 240)

    # def show_product_ordering_widget(self):
    #     self.product_ordering_widget.setDisabled(False)
    #     self.product_ordering_widget.show()

    def retrieve_order(self):
        order_repo = self.customer_registration_widget.get_order_repository()
        self.product_ordering_widget = ProductsOrderingWidget(order_repo)
        #order_repo = self.customer_Registration_widget.get_order_repository()
        #self.product_ordering_widget.set_order_repository(order_repo)
        self.layout().addWidget(self.product_ordering_widget)
        self.setGeometry(100, 45, 850, 650)
        self.product_ordering_widget.show()

    def closeEvent(self, event):
        if hasattr(self, "product_ordering_widget") and self.product_ordering_widget.skip_close_confirmation:
            event.accept()
            return
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Exit Confirmation")
        msg.setText("Are you sure you want to close the window?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
