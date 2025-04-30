'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *

class Table(Rectangle):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Rectangle.__init__(self, Point(p1[0], p1[1]), Point(p2[0], p2[1]))

        self.setWidth(0)
        self.setFill(color_rgb(25, 25, 225))
    
    def clicked(self, point: tuple) -> bool:
        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            self.setWidth(5)
            self.setFill(color_rgb(50, 50, 225))
            return True
        return False