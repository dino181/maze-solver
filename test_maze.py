import unittest

from maze import Maze


class MazeTests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertEqual(m1._cells[0][0].center, (5, 5))
        self.assertEqual(m1._cells[0][1].center, (15, 5))
        self.assertEqual(m1._cells[1][0].center, (5, 15))
        self.assertEqual(m1._cells[1][1].center, (15, 15))

    def test_maze_create_cells_different_size(self):
        num_cols = 62
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertEqual(m1._cells[0][0].center, (5, 5))
        self.assertEqual(m1._cells[0][1].center, (15, 5))
        self.assertEqual(m1._cells[1][0].center, (5, 15))
        self.assertEqual(m1._cells[1][1].center, (15, 15))

    def test_maze_create_cells_different_start(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(100, 100, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertEqual(m1._cells[0][0].center, (105, 105))
        self.assertEqual(m1._cells[0][1].center, (115, 105))
        self.assertEqual(m1._cells[1][0].center, (105, 115))
        self.assertEqual(m1._cells[1][1].center, (115, 115))

    def test_maze_create_cells_different_cell_size(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 20, 12)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        self.assertEqual(m1._cells[0][0].center, (10, 6))
        self.assertEqual(m1._cells[0][1].center, (30, 6))
        self.assertEqual(m1._cells[1][0].center, (10, 18))
        self.assertEqual(m1._cells[1][1].center, (30, 18))

    def test_maze_break_entance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 20, 12)
        m1._break_exit_and_entrance()
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_maze_reset_visited_cells(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 20, 12)
        for row in m1._cells:
            for cell in row:
                cell.visited = True

        self.assertTrue(m1._cells[0][0].visited)

        m1._reset_cells_visited()
        for row in m1._cells:
            for cell in row:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
