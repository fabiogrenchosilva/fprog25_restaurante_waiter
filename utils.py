# File containing helper functions and some settings
import os


def load_configs(filepath: str):
    file = open(filepath, 'r')

    for line in file:
        line.strip()
        if line.startswith("*"):
            args = line.split(" ")

            os.environ[args[1]] = args[2]


def relative_to_window_coords(point: tuple) -> tuple:
    x_pos = point[0] * int(os.environ.get("WIN_WIDTH"))
    y_pos = point[1] * int(os.environ.get("WIN_HEIGHT"))

    return (x_pos, y_pos)


def win_to_grid_coords(point: tuple) -> tuple:
    win_width = int(os.environ.get("WIN_WIDTH"))
    win_height = int(os.environ.get("WIN_HEIGHT"))
    grid_width = int(os.environ.get("GRID_WIDTH"))
    grid_height = int(os.environ.get("GRID_HEIGHT"))

    return int((grid_width*point[0])/win_width), int((grid_height*point[1])/win_height)

load_configs("src/salas/sala01.txt")
#print(int(os.environ.get("WIN_WIDTH")))