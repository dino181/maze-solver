import random
import time
from enum import Enum, auto

from cell import Cell
from window import Window


class Directions(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: int | None = None,
    ):

        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window

        if seed is not None:
            random.seed(seed)

        self._cells: list[list[Cell]] = []
        self._create_cells()
        self._draw_cells()

        self._break_exit_and_entrance()
        self._break_walls(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        for col in range(self._num_cols):
            cell_col = []
            for row in range(self._num_rows):
                cell_col.append(
                    Cell(
                        self._window,
                        self._x1 + row * self._cell_size_x,
                        self._y1 + col * self._cell_size_y,
                        self._x1 + (row + 1) * self._cell_size_x,
                        self._y1 + (col + 1) * self._cell_size_y,
                    )
                )
            self._cells.append(cell_col)

    def _draw_cells(self) -> None:
        if self._window is None:
            return

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j, False)

    def _draw_cell(self, i, j, with_animate=True):
        self._cells[i][j].draw("white")
        if with_animate:
            self._animate()

    def _animate(self):
        self._window.redraw()
        time.sleep(0.05)

    def _break_exit_and_entrance(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False
        if self._window is not None:
            self._draw_cell(0, 0)
            self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls(self, i: int, j: int) -> None:
        directions = []
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if self._in_bounds(i + 1, j) and not self._cells[i + 1][j].visited:
            directions.append(Directions.DOWN)
        if self._in_bounds(i - 1, j) and not self._cells[i - 1][j].visited:
            directions.append(Directions.UP)
        if self._in_bounds(i, j + 1) and not self._cells[i][j + 1].visited:
            directions.append(Directions.RIGHT)
        if self._in_bounds(i, j - 1) and not self._cells[i][j - 1].visited:
            directions.append(Directions.LEFT)

        while directions != []:
            direction = random.choice(directions)
            directions.remove(direction)
            match direction:
                case Directions.UP:
                    if not self._cells[i - 1][j].visited:
                        current_cell.has_top_wall = False
                        self._cells[i - 1][j].has_bottom_wall = False
                        self._break_walls(i - 1, j)
                case Directions.DOWN:
                    if not self._cells[i + 1][j].visited:
                        current_cell.has_bottom_wall = False
                        self._cells[i + 1][j].has_top_wall = False
                        self._break_walls(i + 1, j)
                case Directions.LEFT:
                    if not self._cells[i][j - 1].visited:
                        current_cell.has_left_wall = False
                        self._cells[i][j - 1].has_right_wall = False
                        self._break_walls(i, j - 1)
                case Directions.RIGHT:
                    if not self._cells[i][j + 1].visited:
                        current_cell.has_right_wall = False
                        self._cells[i][j + 1].has_left_wall = False
                        self._break_walls(i, j + 1)
                case _:
                    return
        if self._window is not None:
            self._draw_cell(i, j)

    def _in_bounds(self, i: int, j: int):
        return 0 <= i < len(self._cells) and 0 <= j < len(self._cells[i])

    def _reset_cells_visited(self) -> None:
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i: int, j: int):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        if (
            not self._cells[i][j].has_top_wall
            and self._in_bounds(i - 1, j)
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            res = self.solve_r(i - 1, j)
            if not res:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
            else:
                return res

        if (
            not self._cells[i][j].has_bottom_wall
            and self._in_bounds(i + 1, j)
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            res = self.solve_r(i + 1, j)
            if not res:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)
            else:
                return res

        if (
            not self._cells[i][j].has_left_wall
            and self._in_bounds(i, j - 1)
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            res = self.solve_r(i, j - 1)
            if not res:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
            else:
                return res

        if (
            not self._cells[i][j].has_right_wall
            and self._in_bounds(i, j + 1)
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            res = self.solve_r(i, j + 1)
            if not res:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)
            else:
                return res

        return False
