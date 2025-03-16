from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from game import Game
from game_field import GameField


class MainWindow(QMainWindow):
    __field: GameField

    def __init__(self, width=300, height=500) -> None:
        super().__init__()

        self.label: QLabel = QLabel()
        self.__field = GameField(width, height)

        self.label.setPixmap(self.__field)
        self.setCentralWidget(self.label)

    def keyPressEvent(self, event) -> None:
        game: Game = self.__field.game
        if event.key() == Qt.Key_Escape:
            game.deselect_cell()
            self.upd()
        if event.key() == Qt.Key_W:
            game.mv_selection_up()
            self.upd()
        if event.key() == Qt.Key_S:
            game.mv_selection_down()
            self.upd()
        if event.key() == Qt.Key_A:
            game.mv_selection_left()
            self.upd()
        if event.key() == Qt.Key_D:
            game.mv_selection_right()
            self.upd()

    def upd(self):
        self.__field.repaint()
        self.label.setPixmap(self.__field)
