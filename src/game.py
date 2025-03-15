from random import randint


class Game:
    __field: list[list[int]]
    __cell_types_count: int

    __selected_cell: list[int] = [0, 0]

    def __init__(self, row_count: int, col_count: int, cell_types_count: int):
        self.cell_types_count = cell_types_count
        self.generate_field(row_count, col_count)

    @property
    def cell_types_count(self) -> int:
        return self.__cell_types_count

    @cell_types_count.setter
    def cell_types_count(self, n: int) -> None:
        if n <= 0:
            raise ValueError("cell_type_count should be > 0")
        self.__cell_types_count = n

    @property
    def column_count(self) -> int:
        return len(self.__field[0])

    @property
    def row_count(self) -> int:
        return len(self.__field)

    def cell_type(self, row: int, col: int) -> int:
        return self.__field[row][col]

    def generate_field(self, row_count, col_count) -> None:
        if row_count <= 0:
            raise ValueError("col_count should be > 0")

        if col_count <= 0:
            raise ValueError("row_count should be > 0")

        self.__field = list()
        for r in range(row_count):
            self.__field.append(list())
            for c in range(col_count):
                self.__field[r].append(randint(0, self.cell_types_count - 1))

    def deselect_cell(self) -> None:
        self.__selected_cell[0] = -1
        self.__selected_cell[1] = -1

    def select_cell(self, row: int, col: int) -> None:
        if row < 0 or row >= self.row_count - 1:
            raise ValueError("row is out of field")
        if col < 0 or col >= self.column_count - 1:
            raise ValueError("col is out of field")

        self.__selected_cell[0] = row
        self.__selected_cell[1] = col

    def mv_selection_up(self) -> None:
        self.select_cell(self.__selected_cell[0] - 1, self.__selected_cell[1])

    def mv_selection_down(self) -> None:
        self.select_cell(self.__selected_cell[0] + 1, self.__selected_cell[1])

    def mv_selection_right(self) -> None:
        self.select_cell(self.__selected_cell[0], self.__selected_cell[1] + 1)

    def mv_selection_left(self) -> None:
        self.select_cell(self.__selected_cell[0], self.__selected_cell[1] - 1)

    def is_selected_cell(self, r: int, c: int) -> bool:
        if self.__selected_cell[0] < 0 or self.__selected_cell[1] < 0:
            return False
        if (
            (self.__selected_cell[0] == r and self.__selected_cell[1] == c)
            or (self.__selected_cell[0] + 1 == r and self.__selected_cell[1] == c)
            or (self.__selected_cell[0] == r and self.__selected_cell[1] + 1 == c)
            or (self.__selected_cell[0] + 1 == r and self.__selected_cell[1] + 1 == c)
        ):
            return True
        return False
