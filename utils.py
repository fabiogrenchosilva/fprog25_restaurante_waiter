'''

Group n.º 29
Elements:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

Version 28: 22-05-2025 - 12h42

This file containes some helper functions and classes

'''

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

            # Write to an os variable
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


def generate_empty_array(width: int, height: int) -> list[list[int]]:
    """ Returns a all zeros 2D list (width x height) """
    return [[0 for _ in range(width)] for _ in range(height)]


class Button(Rectangle):
    """ Implementation of a button """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, text: str) -> None:
        super().__init__(Point(*p1), Point(*p2))

        self.is_active = False
        self.fuction = lambda: print()

        self.setFill('blue')
        self.setWidth(0)

        self.draw(win)
        self.text = Text(self.getCenter(), text)
        self.text.setTextColor('white')
        self.text.draw(win)
    
    def handle_click(self, point: tuple) -> bool:
        """ Click handler, returns True if button is clicked """
        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            self.is_active ^= 1
            self.fuction()
            return True
        return False

    def set_active(self, active: bool) -> None:
        """ Sets button's state """
        self.is_active = active

        if self.is_active:
            self.setFill('lightblue')
        else:
            self.setFill('blue')
    
    def set_action(self, function) -> None:
        """ Define a function to run when the button is clicked """
        self.fuction = function
    

class Dropdown(Button):
    """ Implementation of dropdown """
    # This implementation could easily be converted to an actual dropdown menu, 
    # but the for the purpose of this application it would not be considered
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, text: str, dropdown_text: list[str]) -> None:
        super().__init__(win, p1, p2, text)
        
        self.win = win
        self.dropdown_text = dropdown_text

        self.draw_elements = []
    
    def handle_click(self, point: tuple) -> bool:
        """ Click handler, returns True if button is clicked """ 
        if not super().handle_click(point):
            return False
        
        self.is_active ^= 1
        
        if self.is_active:
            y = self.p2.y + 50
        
            for line in self.dropdown_text:
                self.draw_elements.append(Text(Point(self.p1.x-50, y), line))
                y+=20
            
            self.rect = Rectangle(Point(self.p1.x-200, self.p2.y), Point(self.p2.x, y))
            self.rect.setFill('white')
            self.rect.draw(self.win)

            for element in self.draw_elements:
                element.draw(self.win)
   
        else:
            self.rect.undraw()
            for element in self.draw_elements:
                element.undraw()
            
        return True

# Load configurations when this file is imported
load_configs("src/salas/sala01.txt")