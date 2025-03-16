from random import randint


class Game:
    class __Cell:
        row: int
        col: int

        def __init__(self, row: int, col: int) -> None:
            self.row = row
            self.col = col

    __field: list[list[int]]
    __cell_types_count: int

    __selected_cell: __Cell = __Cell(0, 0)

    def __init__(self, row_count=10, col_count=6, cell_types_count=1):
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
        self.__selected_cell.row = -1
        self.__selected_cell.col = -1

    def select_cell(self, row: int, col: int) -> None:
        if row < 0 or row >= self.row_count - 1:
            raise ValueError("row is out of field")
        if col < 0 or col >= self.column_count - 1:
            raise ValueError("col is out of field")

        self.__selected_cell.row = row
        self.__selected_cell.col = col

    def mv_selection(self, dx: int, dy: int) -> None:
        if not self.has_selection():
            self.select_cell(0, 0)
            return

        try:
            self.select_cell(
                self.__selected_cell.row - dy, self.__selected_cell.col + dx
            )
        except Exception:
            pass

    def mv_selection_up(self) -> None:
        self.mv_selection(0, 1)

    def mv_selection_down(self) -> None:
        self.mv_selection(0, -1)

    def mv_selection_right(self) -> None:
        self.mv_selection(1, 0)

    def mv_selection_left(self) -> None:
        self.mv_selection(-1, 0)

    def has_selection(self) -> bool:
        return not (self.__selected_cell.row < 0 or self.__selected_cell.col < 0)

    def is_selected_cell(self, r: int, c: int) -> bool:
        if not self.has_selection():
            return False
        if (
            (self.__selected_cell.row == r and self.__selected_cell.col == c)
            or (self.__selected_cell.row + 1 == r and self.__selected_cell.col == c)
            or (self.__selected_cell.row == r and self.__selected_cell.col + 1 == c)
            or (self.__selected_cell.row + 1 == r and self.__selected_cell.col + 1 == c)
        ):
            return True
        return False

    def rotate_selection_counterclockwise(self) -> None:
        r: int = self.__selected_cell.row
        c: int = self.__selected_cell.col
        f: list[list[int]] = self.__field

        f[r][c], f[r + 1][c], f[r + 1][c + 1], f[r][c + 1] = (
            f[r + 1][c],
            f[r + 1][c + 1],
            f[r][c + 1],
            f[r][c],
        )

    def rotate_selection_clockwise(self) -> None:
        r: int = self.__selected_cell.row
        c: int = self.__selected_cell.col
        f: list[list[int]] = self.__field

        f[r][c], f[r + 1][c], f[r + 1][c + 1], f[r][c + 1] = (
            f[r][c + 1],
            f[r][c],
            f[r + 1][c],
            f[r + 1][c + 1],
        )
