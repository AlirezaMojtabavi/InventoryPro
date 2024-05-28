from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from GUI.EditOrder.OrderInformationWidget import OrderInformationWidget
from GUI.EditOrder.EditOrderWidget import EditOrderWidget


class EditOrderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.order_information_widget = None
        self.edit_order_widget = None
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.order_information_widget = OrderInformationWidget()
        self.order_information_widget.confirm_order_button.clicked.connect(
            self.retrieve_order)
        self.layout.addWidget(self.order_information_widget)
        self.setLayout(self.layout)
        self.setWindowTitle('Customer Registration Window')
        self.setGeometry(100, 60, 400, 180)

    def show_edit_order_widget(self):
        self.edit_order_widget.setDisabled(False)
        self.edit_order_widget.show()

    def retrieve_order(self):
        order_repo = self.order_information_widget.get_order_repo()
        self.edit_order_widget = EditOrderWidget(order_repo)
        #order_repo = self.customer_Registration_widget.get_order_repository()
        #self.product_ordering_widget.set_order_repository(order_repo)
        self.layout.addWidget(self.edit_order_widget)
        self.setGeometry(100, 45, 750, 600)
        self.edit_order_widget.show()
