'''

Group n.º 29
Elements:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

Version 31: 27-05-2025 - 11h35

This file containes the Wall and Obstacle classes implementations

'''

from src.packages.graphics import *
from texture import Texture
from random import choice

class Wall(Texture):
    """ Simple wall to act as a obstacle and dividir between tables """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        super().__init__("dark_rock", p1, p2)
        self.draw(win)

class Obstacle(Texture):
    """ User added obstacle """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, duration: float) -> None:
        super().__init__(choice(["wet_floor_sign", "mariokart_banana"]), p1, p2)

        self.duration = duration

        self.draw(win)
    
    def check_colision(self, point: tuple) -> bool:
        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            return True
        return False

    def update(self, dt: float) -> bool:
        """ Update function, serves for undrawing itself """
        self.duration -= dt
        if self.duration < 0:
            self.undraw()
            del self
            return True