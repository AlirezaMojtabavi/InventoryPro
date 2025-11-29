from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from GUI.EditOrder.OrderInformationWidget import OrderInformationWidget
from GUI.ProductsOrderingWidget import ProductsOrderingWidget


class EditOrderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.order_information_widget = None
        self.edit_order_widget = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        self.order_information_widget = OrderInformationWidget()
        self.order_information_widget.confirm_order_button.clicked.connect(
            self.retrieve_order)
        main_layout.addWidget(self.order_information_widget)
        self.setLayout(main_layout)

        self.setWindowTitle("Edit Order Window")
        self.setGeometry(100, 60, 650, 280)

    def show_edit_order_widget(self):
        self.edit_order_widget.setDisabled(False)
        self.edit_order_widget.show()

    def retrieve_order(self):
        order_repo = self.order_information_widget.get_order_repo()
        order_repo.update_order_time()
        self.edit_order_widget = ProductsOrderingWidget(order_repo)
        self.edit_order_widget.update_order_rows()
        self.edit_order_widget.enable_finalization()

        self.layout().addWidget(self.edit_order_widget)
        self.setGeometry(100, 45, 900, 750)
        self.edit_order_widget.show()

    def closeEvent(self, event):
        if (self.edit_order_widget is not None
                and getattr(self.edit_order_widget, "skip_close_confirmation", False)):
            event.accept()
            return

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Exit Confirmation")
        msg.setText("Are you sure you want to close the window?\n"
                    "The current order will be deleted.")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            # delete order from DB
            repo = self.order_information_widget.get_order_repo()
            repo.delete_current_order()
            event.accept()
        else:
            event.ignore()
