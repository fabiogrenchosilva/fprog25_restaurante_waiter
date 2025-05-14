'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''
###
### File containing Wall and Obstacle classes
###

from src.packages.graphics import *

class Wall(Rectangle):
    """ Simple wall to act as a obstacle and dividir between tables """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Rectangle.__init__(self, Point(p1[0], p1[1]), Point(p2[0], p2[1]))

        # Render with specifc properties
        self.setWidth(0)
        self.setFill(color_rgb(210, 180, 140))
        self.draw(win)

class Obstacle(Rectangle):
    """ User added obstacle """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple, duration: float):
        Rectangle.__init__(self, Point(p1[0], p1[1]), Point(p2[0], p2[1]))

        self.duration = duration

        # Render with specifc properties
        self.setWidth(0)
        self.setFill(color_rgb(100, 255, 140))
        self.draw(win)
    
    def update(self, dt: float) -> bool:
        """ Update function, serves for undrawing itself """
        self.duration -= dt
        if self.duration < 0:
            self.undraw()
            del self
            return True