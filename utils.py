'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''
###
### File containing helper functions and some settings
###

import os
from math import sqrt
from src.packages.graphics import Rectangle, Point, GraphWin, Text

def load_configs(filepath: str) -> None:
    """ Helper function to load configurarions of the room file """
    file = open(filepath, 'r')

    for line in file:
        line.strip()
        if line.startswith("*"):
            args = line.split(" ")

            os.environ[args[1]] = args[2]


def relative_to_window_coords(point: tuple) -> tuple:
    """ Helper function to convert relative windows coords to actual window coords """
    x_pos = point[0] * int(os.environ.get("WIN_WIDTH"))
    y_pos = point[1] * int(os.environ.get("WIN_HEIGHT"))

    return (x_pos, y_pos)


def win_to_grid_coords(point: tuple) -> tuple:
    """ Function to convert from window coords to grid coords """
    win_width = int(os.environ.get("WIN_WIDTH"))
    win_height = int(os.environ.get("WIN_HEIGHT"))
    grid_width = int(os.environ.get("GRID_WIDTH"))
    grid_height = int(os.environ.get("GRID_HEIGHT"))

    return (int((grid_width*point[0])/win_width), int((grid_height*point[1])/win_height))


def grid_to_win_coords(point: tuple) -> tuple:
    """ Function to convert from grid coords to window coords """
    win_width = int(os.environ.get("WIN_WIDTH"))
    win_height = int(os.environ.get("WIN_HEIGHT"))
    grid_width = int(os.environ.get("GRID_WIDTH"))
    grid_height = int(os.environ.get("GRID_HEIGHT"))

    return (point[0]*win_width/grid_width, point[1]*win_height/grid_height)


def distance_p2p(p1: tuple, p2: tuple) -> tuple:
    """ Function to calculate cartesian distance from one point to another """
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    return (x_diff, y_diff, sqrt(x_diff**2 + y_diff**2))


class Button(Rectangle):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, text: str) -> None:
        super().__init__(Point(*p1), Point(*p2))

        self.setFill('blue')
        self.setWidth(0)

        self.draw(win)
        self.text = Text(self.getCenter(), text)
        self.text.setTextColor('white')
        self.text.draw(win)
    
    def check_colision(self, point: tuple) -> None:
        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            return True
        return False
    
    def highlight(self, mode: bool):
        if mode:
            self.setFill('lightblue')
        else:
            self.setFill('blue')

        

# Load configurations when this file is imported
load_configs("src/salas/sala01.txt")