from random import randint


class Cell:
    row: int
    col: int

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if self.row == other.row and self.col == other.col:
            return True
        return False

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __str__(self) -> str:
        return f"Cell(r={self.row}, c={self.col})"

    def __repr__(self) -> str:
        return self.__str__()


class Game:

    __field: list[list[int]]
    __cell_types_count: int

    __selected_cell: Cell = Cell(0, 0)

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

    def __cell_neighbours(self, cell: Cell) -> list:
        neighbours: list[Cell] = list()

        if cell.row > 0:
            neighbours.append(Cell(cell.row - 1, cell.col))
        if cell.col > 0:
            neighbours.append(Cell(cell.row, cell.col - 1))
        if cell.row < self.row_count - 1:
            neighbours.append(Cell(cell.row + 1, cell.col))
        if cell.col < self.column_count:
            neighbours.append(Cell(cell.row, cell.col + 1))

        return neighbours

    def __selection(self) -> list[Cell]:
        selection: list[Cell] = [self.__selected_cell]
        selection.append(Cell(self.__selected_cell.row + 1, self.__selected_cell.col))
        selection.append(
            Cell(self.__selected_cell.row + 1, self.__selected_cell.col + 1)
        )
        selection.append(Cell(self.__selected_cell.row, self.__selected_cell.col + 1))

        return selection

    def __same_cell_colors(self, cell1: Cell, cell2: Cell) -> bool:
        return self.__field[cell1.row][cell1.col] == self.__field[cell2.row][cell2.col]

    def scan_add_destruction_cell(
        self, root_cell: Cell, candidates: set[Cell]
    ) -> set[Cell]:
        stack: list[Cell] = [root_cell]
        while stack.__len__() > 0:
            cell: Cell = stack.pop()
            if cell in candidates:
                continue

            candidates.add(cell)
            for neighbour in self.__cell_neighbours(cell):
                if neighbour not in candidates and self.__same_cell_colors(
                    neighbour, cell
                ):
                    stack.append(neighbour)
        return candidates

    def scan_destruction_select(self) -> set[Cell]:
        candidates: set[Cell] = set()
        for selection_cell in self.__selection():
            self.scan_add_destruction_cell(selection_cell, candidates)

        return candidates
