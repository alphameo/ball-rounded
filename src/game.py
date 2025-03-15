from random import randint


class Game:
    __field: list[list[int]]
    __cell_types_count: int

    __selected_cell: tuple[int, int] = (-1, -1)

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
