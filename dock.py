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

class Dock(Rectangle):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Rectangle.__init__(self, Point(p1[0], p1[1]), Point(p2[0], p2[1]))
        self.win = win

        self.setWidth(1)
        self.setFill(color_rgb(210, 180, 140))

        self.draw(win)
