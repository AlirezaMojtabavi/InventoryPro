import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QLabel

class DesktopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Desktop Window")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Right-click here!", self)
        self.label.setGeometry(50, 50, 300, 200)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        view_action = QAction("View", self)
        view_menu = QMenu(self)
        view_menu.addAction("Option 1")
        view_menu.addAction("Option 2")
        view_action.setMenu(view_menu)

        refresh_action = QAction("Refresh", self)

        context_menu.addAction(view_action)
        context_menu.addAction(refresh_action)

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == view_action:
            # Handle view action
            pass
        elif action == refresh_action:
            # Handle refresh action
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopWindow()
    window.show()
    sys.exit(app.exec_())