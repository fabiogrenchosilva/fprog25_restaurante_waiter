'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''
###
### File containing Dock class for the charging station and the plate delivery
###

from src.packages.graphics import *
from texture import Texture

class Dock(Texture):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        super().__init__("roomba_dock", p1, p2)

        self.draw(win)

class Plates(Texture):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        super().__init__("dark_rock", p1, p2)

        self.draw(win)
