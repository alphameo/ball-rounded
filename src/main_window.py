from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt
from game import Game
from game_renderer import GameRenderer


class MainWindow(QMainWindow):
    __game_window: GameRenderer

    def __init__(self, width=300, height=500) -> None:
        super().__init__()

        self.label: QLabel = QLabel()
        self.__game_window = GameRenderer(width, height, Game(cell_types_count=4))

        self.label.setPixmap(self.__game_window)
        self.setCentralWidget(self.label)

    def keyPressEvent(self, event) -> None:
        g: Game = self.__game_window.game
        if event.key() == Qt.Key_Escape:
            g.deselect_cell()
            self.upd()
        if event.key() == Qt.Key_W:
            g.mv_selection_up()
            self.upd()
        if event.key() == Qt.Key_S:
            g.mv_selection_down()
            self.upd()
        if event.key() == Qt.Key_A:
            g.mv_selection_left()
            self.upd()
        if event.key() == Qt.Key_D:
            g.mv_selection_right()
            self.upd()

    def upd(self):
        self.__game_window.repaint()
        self.label.setPixmap(self.__game_window)
