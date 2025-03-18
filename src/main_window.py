from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import QTimer, Qt
from game import Cell, Game
from game_renderer import GameRenderer


class MainWindow(QMainWindow):
    __game_window: GameRenderer

    def __init__(self, width=300, height=500) -> None:
        super().__init__()

        self.label: QLabel = QLabel()
        self.__game_window = GameRenderer(width, height, Game(cell_types_count=4))
        # print(self.__game_window.game.destroy_field_clusters())

        self.label.setPixmap(self.__game_window)
        self.setCentralWidget(self.label)

    def keyPressEvent(self, event) -> None:
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
            self.upd()
        if event.key() == Qt.Key.Key_Q:
            g.rotate_selection_clockwise()
            self.upd()
        if event.key() == Qt.Key.Key_X:
            print(self.__game_window.game.destroy_field_clusters())
            self.upd()
        if event.key() == Qt.Key.Key_C:
            print(g.ascend_rows())
            self.upd()
        if event.key() == Qt.Key.Key_Z:
            self.destruction_loop(0.2)
        # if event.key() == Qt.Key.Key_L:
        #     while True:
        #         t.sleep(0.2)
        #         print(1)


    # INFO: inner func instead of while loop because event loop blocking
    def destruction_loop(self, time_sleep: float) -> None:
        destroyed = self.__game_window.game.destroy_field_clusters()
        self.upd()
        print(f"start: {destroyed=}")

        def update_and_check():
            nonlocal destroyed
            destroyed -= self.__game_window.game.ascend_rows()
            self.upd()
            print(destroyed)

            if destroyed <= 0:
                self.timer.stop()

        self.timer = QTimer()
        self.timer.timeout.connect(update_and_check)
        self.timer.start(int(time_sleep * 1000))

    def upd(self):
        # print(self.__game_window.game.destroy_field_clusters())
        self.__game_window.repaint()
        self.label.setPixmap(self.__game_window)
