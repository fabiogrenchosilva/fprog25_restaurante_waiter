'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *

class Table():
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):

        self.rectangle = Rectangle(Point(p1[0], p1[1]), Point(p2[0], p2[1]))
        self.win = win

        self.rectangle.setWidth(0)
        self.rectangle.setFill(color_rgb(25, 25, 225))

    
    def draw(self):
        self.rectangle.draw(self.win)

    def undraw(self):
        self.rectangle.undraw()


    
