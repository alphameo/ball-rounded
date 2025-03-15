from PyQt5 import QtWidgets

from game_field import GameField


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, width=300, height=500) -> None:
        super().__init__()

        self.label: QtWidgets.QLabel = QtWidgets.QLabel()
        field: GameField = GameField(width, height)
        self.label.setPixmap(field)
        self.setCentralWidget(self.label)
