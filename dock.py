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
from utils import generate_texture

class Dock(Texture):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Texture.__init__(self, "wood_texture", p1, p2)
        # self.win = win

        # texture = generate_texture("marble", p1, p2)
        # texture.draw(win)

        # self.setWidth(10)
        # self.setFill(color_rgb(210, 180, 140))

        self.draw(win)
