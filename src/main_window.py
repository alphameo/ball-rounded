from PyQt5.QtCore import QEventLoop, Qt, QTimer
from PyQt5.QtWidgets import QLabel, QMainWindow

from game import Game
from game_renderer import GameRenderer


class MainWindow(QMainWindow):
    __game_window: GameRenderer
    __timer: QTimer = QTimer()

    def __init__(self, width=300, height=500) -> None:
        super().__init__()

        self.label: QLabel = QLabel()
        self.__game_window = GameRenderer(width, height, Game(cell_types_count=4))
        # print(self.__game_window.game.destroy_field_clusters())

        self.label.setPixmap(self.__game_window)
        self.setCentralWidget(self.label)

    def keyPressEvent(self, event) -> None:
        if self.__timer.isActive():
            return

        g: Game = self.__game_window.game
        if event.key() == Qt.Key.Key_Escape:
            g.deselect_cell()
            self.upd()
        if event.key() == Qt.Key.Key_W:
            g.mv_selection_up()
            self.upd()
        if event.key() == Qt.Key.Key_S:
            g.mv_selection_down()
            self.upd()
        if event.key() == Qt.Key.Key_A:
            g.mv_selection_left()
            self.upd()
        if event.key() == Qt.Key.Key_D:
            g.mv_selection_right()
            self.upd()
        if event.key() == Qt.Key.Key_E:
            g.rotate_selection_counterclockwise()
            self.animated_destruction(300)
        if event.key() == Qt.Key.Key_Q:
            g.rotate_selection_clockwise()
            self.animated_destruction(300)

    # INFO: inner func instead of while loop because event loop blocking
    def animated_destruction(self, time_sleep_ms: int) -> None:
        self.upd()
        destroyed = self.__game_window.game.destroy_field_clusters()
        self.animate_ascending(destroyed, time_sleep_ms)


        # def animation() -> None:
        #     nonlocal destroyed
        #     self.animate_ascending(destroyed, time_sleep_ms)
        #     destroyed = self.__game_window.game.destroy_field_clusters()
        #     if destroyed <= 0:
        #         loop.quit()
        #     else:
        #         QTimer.singleShot(time_sleep_ms * 2, animation)
        #
        # loop = QEventLoop()
        # QTimer.singleShot(time_sleep_ms * 2, animation)
        # loop.exec_()
        # def destruction_loop(self, time_sleep: int) -> None:

    def animate_ascending(self, destroyed: int, time_sleep_ms: int) -> None:
        def animation_frame():
            nonlocal destroyed
            destroyed -= self.__game_window.game.ascend_rows()
            self.upd()

            if destroyed <= 0:
                self.__timer.stop()

        self.__timer = QTimer()
        self.__timer.timeout.connect(animation_frame)
        self.__timer.start(time_sleep_ms)

    def upd(self):
        # print(self.__game_window.game.destroy_field_clusters())
        self.__game_window.repaint()
        self.label.setPixmap(self.__game_window)
