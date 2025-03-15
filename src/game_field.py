from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt

from random import randint

DEFAULT_COLOR_PALLETE: list[Qt.GlobalColor] = [
    Qt.GlobalColor.blue,
    Qt.GlobalColor.red,
    Qt.GlobalColor.green,
    Qt.GlobalColor.cyan,
]

SELECTION_COLOR: Qt.GlobalColor = Qt.GlobalColor.black


class GameField(QtGui.QPixmap):
    __color_pallete: list[Qt.GlobalColor]

    __mesh_width: int
    __mesh_height: int

    __cell_height: int
    __cell_width: int
    __cell_height_rad: float
    __cell_width_rad: float
    __cell_width_offset: int
    __cell_height_offset: int

    __field: list[list[int]]

    def __init__(
        self,
        width: int,
        height: int,
        row_count=10,
        col_count=6,
        color_pallete=DEFAULT_COLOR_PALLETE,
    ):
        super().__init__(width, height)

        self.__color_pallete = color_pallete

        self.fill(Qt.GlobalColor.white)

        self.generate_field(row_count, col_count)
        # self.draw_something()
        self.draw()

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

        self.__color_pallete = color_pallete

    @property
    def column_count(self) -> int:
        return len(self.__field[0])

    @property
    def row_count(self) -> int:
        return len(self.__field)

    def __calc_cell_sizes(self) -> None:
        self.__mesh_width = int(self.width() / self.column_count)
        self.__mesh_height = int(self.height() / self.row_count)
        self.__cell_height_offset = int(self.__mesh_height * 0.1)
        self.__cell_width_offset = int(self.__mesh_width * 0.1)
        self.__cell_width = self.__mesh_width - 2 * self.__cell_width_offset
        self.__cell_height = self.__mesh_height - 2 * self.__cell_height_offset

        self.__cell_height_rad = self.__cell_height / 2
        self.__cell_width_rad = self.__cell_width / 2

    def generate_field(self, row_count, col_count):
        if row_count <= 0:
            raise ValueError("col_count should be > 0")

        if col_count <= 0:
            raise ValueError("row_count should be > 0")

        self.__field = list()
        for r in range(row_count):
            self.__field.append(list())
            for c in range(col_count):
                self.__field[r].append(randint(0, self.color_pallete.__len__() - 1))

        self.__calc_cell_sizes()

    def draw(self) -> None:
        painter = QtGui.QPainter(self)
        for r in range(self.row_count):
            for c in range(self.column_count):
                self.__draw_cell(r, c, self.color_pallete[self.__field[r][c]], painter)
        painter.end()

    def __draw_cell(
        self,
        row: int,
        column: int,
        color: Qt.GlobalColor,
        painter: QtGui.QPainter,
        is_active=False,
    ):
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

        pen_color = SELECTION_COLOR if is_active else color
        pen: QtGui.QPen = QtGui.QPen(pen_color, 2)
        painter.setPen(pen)
        painter.fillPath(
            path,
            color,
        )
        painter.drawPath(path)
