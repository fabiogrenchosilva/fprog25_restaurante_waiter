'''

Group n.º 29
Elements:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

Version 31: 27-05-2025 - 11h35

This file containes the implementation of Dock and Plates classes

'''

from src.packages.graphics import *
from texture import Texture

class Dock(Texture):
    """ Implementation of a charging dock for the waiter class """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        super().__init__("roomba_dock", p1, p2)

        self.draw(win)

class Plates(Texture):
    """ Implementation of a plates delivery for the waiter class """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        super().__init__("dark_rock", p1, p2)

        self.draw(win)
