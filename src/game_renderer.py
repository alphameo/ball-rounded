from copyreg import constructor
from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt


from game import Cell, Game

DEFAULT_COLOR_PALLETE: list[Qt.GlobalColor] = [
    Qt.GlobalColor.magenta,
    Qt.GlobalColor.blue,
    Qt.GlobalColor.red,
    Qt.GlobalColor.green,
    Qt.GlobalColor.cyan,
]

SELECTION_COLOR: Qt.GlobalColor = Qt.GlobalColor.black


class GameRenderer(QtGui.QPixmap):
    __color_pallete: list[Qt.GlobalColor]

    __mesh_width: int
    __mesh_height: int

    __cell_height: int
    __cell_width: int
    __cell_height_rad: float
    __cell_width_rad: float
    __cell_width_offset: int
    __cell_height_offset: int

    __game: Game

    def __init__(
        self,
        width: int,
        height: int,
        game: Game,
        color_pallete=DEFAULT_COLOR_PALLETE,
    ):
        super().__init__(width, height)

        self.__game = game
        self.color_pallete = color_pallete

        self.__calc_cell_sizes()
        self.repaint()

    @property
    def color_pallete(self) -> list[Qt.GlobalColor]:
        return self.__color_pallete

    @color_pallete.setter
    def color_pallete(self, color_pallete: list[Qt.GlobalColor]) -> None:
        if color_pallete.__len__() == 0:
            raise ValueError("count of colors in color_pallete should be > 0")
        if not isinstance(color_pallete, list) or not isinstance(
            color_pallete[0], Qt.GlobalColor
        ):
            raise TypeError("color_pallete should be of type list[Qt.GlobalColor]")

        self.__validate_colors(color_pallete)

        self.__color_pallete = color_pallete

    def __validate_colors(self, color_pallete: list[Qt.GlobalColor]) -> None:
        if color_pallete.__len__() < self.game.cell_types_count:
            raise ValueError(
                "count of colors in color_pallete < count of game color types"
            )

    @property
    def column_count(self) -> int:
        return self.game.column_count

    @property
    def row_count(self) -> int:
        return self.game.row_count

    @property
    def game(self) -> Game:
        return self.__game

    def __calc_cell_sizes(self) -> None:
        self.__mesh_width = int(self.width() / self.column_count)
        self.__mesh_height = int(self.height() / self.row_count)
        self.__cell_height_offset = int(self.__mesh_height * 0.1)
        self.__cell_width_offset = int(self.__mesh_width * 0.1)
        self.__cell_width = self.__mesh_width - 2 * self.__cell_width_offset
        self.__cell_height = self.__mesh_height - 2 * self.__cell_height_offset

        self.__cell_height_rad = self.__cell_height / 2
        self.__cell_width_rad = self.__cell_width / 2

    def repaint(self) -> None:
        non_existant = self.game.detect_selection_destruction()
        self.__validate_colors(self.color_pallete)
        self.fill(Qt.GlobalColor.white)
        painter = QtGui.QPainter(self)
        for r in range(self.row_count):
            for c in range(self.column_count):
                color = (
                    None
                    if Cell(r, c) in non_existant
                    else self.color_pallete[self.game.cell_type(r, c)]
                )
                self.__draw_cell(r, c, color, painter)
        painter.end()

    def __draw_cell(
        self,
        row: int,
        column: int,
        color: Qt.GlobalColor | None,
        painter: QtGui.QPainter,
    ) -> None:
        x: int = column * self.__mesh_width + self.__cell_height_offset
        y: int = row * self.__mesh_height + self.__cell_width_offset
        path = QtGui.QPainterPath()
        path.addRoundedRect(
            QRectF(
                x,
                y,
                self.__cell_width,
                self.__cell_height,
            ),
            self.__cell_width_rad,
            self.__cell_height_rad,
        )

        if color is not None:
            painter.fillPath(
                path,
                color,
            )

        if self.game.is_selected_cell(row, column):
            pen_color = SELECTION_COLOR
            pen: QtGui.QPen = QtGui.QPen(pen_color, 3)
            painter.setPen(pen)
            painter.drawPath(path)
