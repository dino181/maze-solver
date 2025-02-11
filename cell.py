from typing import Self

from line import Line, Point
from window import Window


class Cell:
    def __init__(self, window: Window, x1: int, y1: int, x2: int, y2: int) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__window = window

        self.has_top_wall = True
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.center = ((x1 + x2) / 2, (y1 + y2) / 2)
        self.visited = False

    def draw(self, color: str) -> None:
        default_color = "black"
        line_color = color if self.has_top_wall else default_color
        line = Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1))
        self.__window.draw_line(line, line_color)

        line_color = color if self.has_left_wall else default_color
        line = Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2))
        self.__window.draw_line(line, line_color)

        line_color = color if self.has_right_wall else default_color
        line = Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2))
        self.__window.draw_line(line, line_color)

        line_color = color if self.has_bottom_wall else default_color
        line = Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2))
        self.__window.draw_line(line, line_color)

    def draw_move(self, to_cell: Self, undo=False):
        color = "grey" if undo else "red"
        line = Line(
            Point(self.center[0], self.center[1]),
            Point(to_cell.center[0], to_cell.center[1]),
        )
        self.__window.draw_line(line, color)
