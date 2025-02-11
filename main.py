from maze import Maze
from window import Window


def main():
    win = Window(800, 800)
    maze = Maze(30, 30, 25, 25, 30, 30, win)

    solved = maze.solve()
    if solved:
        print("Solved the maze!")
    else:
        print("Could not solve this maze.")

    win.wait_for_close()


if __name__ == "__main__":
    main()
