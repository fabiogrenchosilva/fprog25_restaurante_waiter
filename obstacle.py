'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *

class Obstacle():
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):

        self.rectangle = Rectangle(Point(p1[0], p1[1]), Point(p2[0], p2[1]))
        self.win = win

        self.rectangle.setWidth(0)
        self.rectangle.setFill(color_rgb(210, 180, 140))


    def draw(self):
        self.rectangle.draw(self.win)

    def undraw(self):
        self.rectangle.undraw(self.win)