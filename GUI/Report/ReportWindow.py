# GUI/Report/ReportWindow.py
import subprocess

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from GUI.Report.ReportWidget import ReportWidget
from Repositories.OrderRepository import OrderRepository
from Reports.InvoicePdf import InvoicePdf


class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Report")
        self.setGeometry(120, 80, 420, 380)

        self.order_repo = OrderRepository()

        layout = QVBoxLayout(self)
        self.report_widget = ReportWidget()
        layout.addWidget(self.report_widget)
        self.setLayout(layout)

        self.report_widget.date_range_selected.connect(self.generate_report)

    def generate_report(self, start_dt, end_dt):
        rows = self.order_repo.get_product_summary_between(start_dt, end_dt)

        if not rows:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("No Data")
            msg.setText("There are no orders in the selected date range.")
            msg.exec_()
            return

        pdf_generator = InvoicePdf()
        output_path = pdf_generator.build_report(rows, start_dt, end_dt)

        subprocess.Popen(["start", output_path], shell=True)
