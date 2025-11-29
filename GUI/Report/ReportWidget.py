# GUI/Report/ReportWidget.py
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
    QRadioButton, QFormLayout, QDateEdit, QFrame
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from GUI.Styles import REPORT_BUTTON_STYLE, DATE_CARD_STYLE, REPORT_RADIO_STYLE, REPORT_DATEEDIT_STYLE, \
    APP_REPORT_STYLE
from PyQt5.QtGui import QFont


class ReportWidget(QWidget):
    date_range_selected = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Report")
        self.setMinimumSize(420, 380)
        self.setStyleSheet(APP_REPORT_STYLE + DATE_CARD_STYLE)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        # ---- Title ----
        title_label = QLabel("Sales Report")
        title_font = QFont("Segoe UI", 17, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        subtitle = QLabel("Select a date range for the report")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666666; font-size: 9pt;")
        main_layout.addWidget(subtitle)

        # ---- Card ----
        card = QFrame()
        card.setObjectName("DateCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 10)
        card_layout.setSpacing(10)

        # card header
        header = QLabel("Date range")
        header.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        card_layout.addWidget(header)

        # radios
        self.today_radio = QRadioButton("Today")
        self.custom_radio = QRadioButton("Custom range")

        self.today_radio.setStyleSheet(REPORT_RADIO_STYLE)
        self.custom_radio.setStyleSheet(REPORT_RADIO_STYLE)

        radios_row = QHBoxLayout()
        radios_row.setSpacing(18)
        radios_row.addWidget(self.today_radio)
        radios_row.addWidget(self.custom_radio)
        radios_row.addStretch(1)

        card_layout.addLayout(radios_row)
        card_layout.addSpacing(10)

        # date edits as a compact form
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFormAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(14)
        form_layout.setContentsMargins(5, 8, 5, 12)

        label_font = QFont("Segoe UI", 9)

        from_label = QLabel("From:")
        till_label = QLabel("Till:")
        from_label.setFont(label_font)
        till_label.setFont(label_font)
        from_label.setMinimumWidth(40)
        till_label.setMinimumWidth(40)

        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        self.from_date.setDate(QDate.currentDate())
        self.from_date.setEnabled(False)
        self.from_date.setStyleSheet(REPORT_DATEEDIT_STYLE)

        self.till_date = QDateEdit()
        self.till_date.setCalendarPopup(True)
        self.till_date.setDate(QDate.currentDate())
        self.till_date.setEnabled(False)
        self.till_date.setStyleSheet(REPORT_DATEEDIT_STYLE)

        form_layout.addRow(from_label, self.from_date)
        form_layout.addRow(till_label, self.till_date)

        card_layout.addLayout(form_layout)
        card_layout.addStretch(1)
        main_layout.addWidget(card)

        main_layout.addStretch(1)

        # ---- Button ----
        self.confirm_button = QPushButton("Generate report")
        self.confirm_button.setFixedSize(230, 42)
        self.confirm_button.setEnabled(False)
        self.confirm_button.setStyleSheet(REPORT_BUTTON_STYLE)
        self.confirm_button.clicked.connect(self.on_confirm)

        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

        # connections
        self.today_radio.toggled.connect(self.on_radio_changed)
        self.custom_radio.toggled.connect(self.on_radio_changed)

        # default selection
        self.today_radio.setChecked(True)

    def on_radio_changed(self):
        if self.today_radio.isChecked():
            # Today: disable date edits
            self.from_date.setEnabled(False)
            self.till_date.setEnabled(False)
            today = QDate.currentDate()
            self.from_date.setDate(today)
            self.till_date.setDate(today)
            self.confirm_button.setEnabled(True)
        elif self.custom_radio.isChecked():
            # Custom: enable date edits
            self.from_date.setEnabled(True)
            self.till_date.setEnabled(True)
            self.confirm_button.setEnabled(True)
        else:
            self.confirm_button.setEnabled(False)

    def _qdate_to_datetime(self, qdate: QDate) -> datetime:
        return datetime(qdate.year(), qdate.month(), qdate.day())

    def on_confirm(self):
        if self.today_radio.isChecked():
            q = QDate.currentDate()
            start_date = q.toPyDate()
            end_date = q.toPyDate()
        else:
            from_q = self.from_date.date()
            till_q = self.till_date.date()
            start_date = from_q.toPyDate()
            end_date = till_q.toPyDate()

        self.date_range_selected.emit(start_date, end_date)
