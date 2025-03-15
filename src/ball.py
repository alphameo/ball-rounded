from PyQt5.QtCore import Qt


class Ball:
    __color: Qt.GlobalColor

    def __init__(self, color: Qt.GlobalColor) -> None:
        self.__color = color

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: Qt.GlobalColor):
        if not isinstance(color, Qt.GlobalColor):
            raise TypeError("Color should be of type GlobalColor")
        self.__color = color
