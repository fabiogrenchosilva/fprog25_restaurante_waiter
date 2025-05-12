# File containing helper functions and some settings
import os
from math import sqrt

def load_configs(filepath: str) -> None:
    file = open(filepath, 'r')

    for line in file:
        line.strip()
        if line.startswith("*"):
            args = line.split(" ")

            os.environ[args[1]] = args[2]


def relative_to_window_coords(point: tuple) -> tuple:
    """Helper function to convert relative windows coords to actual window coords"""
    x_pos = point[0] * int(os.environ.get("WIN_WIDTH"))
    y_pos = point[1] * int(os.environ.get("WIN_HEIGHT"))

    return (x_pos, y_pos)


def win_to_grid_coords(point: tuple) -> tuple:
    """Function to convert from window coords to grid coords"""
    win_width = int(os.environ.get("WIN_WIDTH"))
    win_height = int(os.environ.get("WIN_HEIGHT"))
    grid_width = int(os.environ.get("GRID_WIDTH"))
    grid_height = int(os.environ.get("GRID_HEIGHT"))

    return (int((grid_width*point[0])/win_width), int((grid_height*point[1])/win_height))


def grid_to_win_coords(point: tuple) -> tuple:
    """Function to convert from grid coords to window coords"""
    win_width = int(os.environ.get("WIN_WIDTH"))
    win_height = int(os.environ.get("WIN_HEIGHT"))
    grid_width = int(os.environ.get("GRID_WIDTH"))
    grid_height = int(os.environ.get("GRID_HEIGHT"))

    return (point[0]*win_width/grid_width, point[1]*win_height/grid_height)


def distance_p2p(p1: tuple, p2: tuple) -> tuple:
    """Function to calculate cartesian distance from one point to another"""
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    return (x_diff, y_diff, sqrt(x_diff**2 + y_diff**2))


load_configs("src/salas/sala01.txt")