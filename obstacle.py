'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *

class Wall(Rectangle):
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Rectangle.__init__(self, Point(p1[0], p1[1]), Point(p2[0], p2[1]))

        self.setWidth(0)
        self.setFill(color_rgb(210, 180, 140))

class Obstacle(Rectangle):
    def __init__(self, point: tuple):
        super().__init__(Point(point[0]-25, point[1]-25), Point(point[0]+25, point[1]+25))

        self.setFill(color_rgb(0, 180, 140))

        self.duration = 3.0
    
    def update(self, dt):
        self.duration -= dt
        return self.duration <= 0
