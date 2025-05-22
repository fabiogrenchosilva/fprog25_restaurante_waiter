'''

Group n.º 29
Elements:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

Version 28: 22-05-2025 - 12h42

This file containes the Wall and Obstacle classes implementations

'''

from src.packages.graphics import *
from texture import Texture

class Wall(Texture):
    """ Simple wall to act as a obstacle and dividir between tables """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Texture.__init__(self, "dark_rock", p1, p2)
        self.draw(win)

class Obstacle(Texture):
    """ User added obstacle """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, duration: float):
        Texture.__init__(self, "wet_floor_sign", p1, p2)

        self.duration = duration

        # Render with specifc properties
        # self.setWidth(0)
        # self.setFill(color_rgb(100, 255, 140))
        self.draw(win)
    
    def update(self, dt: float) -> bool:
        """ Update function, serves for undrawing itself """
        self.duration -= dt
        if self.duration < 0:
            self.undraw()
            del self
            return True