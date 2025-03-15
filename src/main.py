import sys

from PyQt5.QtWidgets import QApplication, QWidget

from main_window import MainWindow

if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    window: QWidget = MainWindow()
    window.show()
    app.exec()
