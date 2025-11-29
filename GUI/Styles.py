from PyQt5.QtGui import QFont

MAIN_BUTTON_STYLE = """
QPushButton {
    background-color: black;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 24px;
}
QPushButton:hover {
    background-color: #2980b9;
}
"""

MAIN_FONT = QFont("Arial", 12, QFont.Bold)
MAIN_BG_COLOR = "#f0f0f0"
MAIN_BUTTON_SIZE = (300, 100)

CUSTOMER_INPUT_STYLE = """
QLineEdit {
    font-weight: bold;
    background-color: #f7f7f7;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12pt;
}
QLineEdit:disabled {
    background-color: #e9e9e9;
    color: #777777;
}
"""

CUSTOMER_CONFIRM_BUTTON_STYLE = """
QPushButton {
    background-color: #28a745;
    color: white;
    border-radius: 14px;
    padding: 8px 18px;
    font-size: 11pt;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #218838;
}
QPushButton:pressed {
    background-color: #1e7e34;
}
QPushButton:disabled {
    background-color: #bfbfbf;   /* GRAY background when disabled */
    color: #6b6b6b;              /* Slightly darker text */
}
"""

CUSTOMER_GROUPBOX_STYLE = """
QGroupBox {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
"""

CUSTOMER_LABEL_FONT = QFont("Arial", 12, QFont.Bold)

ORDER_TABLE_STYLE = """
QTableWidget {
    background-color: #ffffff;
    border: none;
}

/* Normal cell appearance */
QTableWidget::item {
    padding: 5px;
}

/* Selected row */
QTableWidget::item:selected {
    background-color: #c0c0c0;
}

/* Alternating rows */
QTableWidget::item:alternate {
    background-color: #f0f0f0;
}
"""

# ---------- Product Ordering styles ----------

ORDER_GROUPBOX_STYLE = """
QGroupBox {
    font-weight: bold;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    margin-top: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    font-weight: normal;
}
"""

ORDER_CHOOSE_BUTTON_STYLE = """
QPushButton {
    background-color: #007BFF;
    color: white;
    border-radius: 8px;
    padding: 8px 24px;
    font-size: 18px;
    font-weight: bold;
}
QPushButton:hover:!disabled {
    background-color: #0069d9;
}
QPushButton:pressed:!disabled {
    background-color: #0053ba;
}
QPushButton:disabled {
    background-color: #d0d0d0;
    color: #888888;
}
"""

ORDER_FINALIZE_BUTTON_STYLE = """
QPushButton {
    background-color: #d0d0d0;
    color: #888888;
    border-radius: 8px;
    padding: 8px 24px;
    font-size: 18px;
    font-weight: bold;
}

/* When ENABLED */
QPushButton:enabled {
    background-color: #1abc9c;  /* Mint Green */
    color: white;
}

/* Hover when enabled */
QPushButton:hover:enabled {
    background-color: #16a085;
}

/* Pressed */
QPushButton:pressed:enabled {
    background-color: #138d75;
}

/* Disabled stays Gray */
QPushButton:disabled {
    background-color: #d0d0d0;
    color: #aaaaaa;
}
"""

# ---------- Category menu styles ----------

CATEGORY_MENU_STYLE = """
QMenu {
    background-color: #ffffff;
    border: 1px solid #c0c0c0;
    padding: 4px;
}

/* Normal items */
QMenu::item {
    padding: 8px 32px 8px 16px;   /* top/right/bottom/left */
    font-size: 12pt;
    font-weight: bold;
    color: #000000;
}

/* Hover / selected item */
QMenu::item:selected {
    background-color: #007BFF;
    color: #ffffff;
}

/* Optional: separator lines */
QMenu::separator {
    height: 1px;
    background: #e0e0e0;
    margin: 4px 0;
}
"""