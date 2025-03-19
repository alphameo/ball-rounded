from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QBoxLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from game import Game
from game_renderer import GameRenderer


class MainWindow(QMainWindow):
    __game_window: GameRenderer
    __label_wrapper: QLabel
    __timer: QTimer = QTimer()
    __label_score: QLabel
    __g_width: int
    __g_height: int

    def __init__(self, width=300, height=500) -> None:
        super().__init__()
        self.__g_width = width
        self.__g_height = height
        self.setWindowTitle("B'All-Rounded Game")

        self.__init_game()

        main_widget: QWidget = QWidget()
        self.setCentralWidget(main_widget)

        layout: QHBoxLayout = QHBoxLayout(main_widget)

        self.__label_wrapper = QLabel()
        self.__label_wrapper.setPixmap(self.__game_window)

        layout.addWidget(self.__label_wrapper)

        font = self.font()
        font.setPointSize(18)
        self.__label_score = QLabel()
        self.__label_score.setFont(font)
        menu_layout: QVBoxLayout = QVBoxLayout()
        menu_layout.addWidget(self.__label_score)

        button = QPushButton(text="RESTART GAME")
        button.setFont(font)
        button.clicked.connect(self.__restart_game)
        menu_layout.addWidget(button)

        layout.addLayout(menu_layout)
        self.upd()

    def __init_game(self) -> None:
        game: Game = Game(cell_types_count=4)
        game.shuffle_field(100)
        self.__game_window = GameRenderer(self.__g_width, self.__g_height, game)

    def __restart_game(self) -> None:
        self.__init_game()
        self.upd()
        self.__timer.stop()

    def keyPressEvent(self, event) -> None:

        g: Game = self.__game_window.game
        if event.key() == Qt.Key.Key_Escape:
            g.deselect_cell()
            self.upd()
            return
        if event.key() == Qt.Key.Key_W:
            g.mv_selection_up()
            self.upd()
            return
        if event.key() == Qt.Key.Key_S:
            g.mv_selection_down()
            self.upd()
            return
        if event.key() == Qt.Key.Key_A:
            g.mv_selection_left()
            self.upd()
            return
        if event.key() == Qt.Key.Key_D:
            g.mv_selection_right()
            self.upd()
            return

        if self.__timer.isActive():
            return

        if event.key() == Qt.Key.Key_E:
            g.rotate_selection_counterclockwise()
            self.animated_destruction(300)
            return
        if event.key() == Qt.Key.Key_Q:
            g.rotate_selection_clockwise()
            self.animated_destruction(300)
            return

    def animated_destruction(self, time_sleep_ms: int) -> None:
        self.upd()
        destroyed = self.__game_window.game.destroy_field_clusters()
        QTimer.singleShot(time_sleep_ms * 3, self.upd)
        self.animate_ascending(destroyed, time_sleep_ms)

    # INFO: timer instead of while loop because event loop blocking
    def animate_ascending(self, destroyed: int, time_sleep_ms: int) -> None:
        def animation_frame():
            nonlocal destroyed
            if destroyed <= 0:
                self.__timer.stop()
                return

            destroyed -= self.__game_window.game.ascend_rows()
            self.upd()

            if destroyed <= 0:
                self.animate_ascending(
                    self.__game_window.game.destroy_field_clusters(), time_sleep_ms
                )

        self.__timer = QTimer()
        self.__timer.timeout.connect(animation_frame)
        self.__timer.start(time_sleep_ms)

    def upd(self):
        self.__game_window.repaint()
        self.__label_wrapper.setPixmap(self.__game_window)
        self.__label_score.setText(
            f"score: {self.__game_window.game.quant_destructions}"
        )
