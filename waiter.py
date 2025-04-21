from src.packages.graphics import *
from time import sleep
from math import sqrt

class Waiter(Circle):
    def __init__(self, win: GraphWin, pos: tuple):
        Circle.__init__(self, Point(*pos), 25)

        self.current_pos = pos
        self.pos_to_go = pos

        self.velocity = 200 # px/s

        self.setWidth(1)
        self.setFill(color_rgb(255, 0, 0))

    def move_to(self, point: tuple):
        self.pos_to_go = point
    
    def _move_yha(self, dt):
        x_diff, y_diff, distance = distance_p2p(self.pos_to_go, self.current_pos)
        if distance > 2:
            x_norm = x_diff / distance * self.velocity * dt
            y_norm = y_diff / distance * self.velocity * dt

            self.move(x_norm, y_norm)
            self.current_pos = (self.current_pos[0]+x_norm, self.current_pos[1]+y_norm)

        else:
            self.current_pos = self.pos_to_go
    
    def update(self, dt):

        self._move_yha(dt)
        
    


def distance_p2p(p1: tuple, p2: tuple) -> tuple:
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    return (x_diff, y_diff, sqrt(x_diff**2 + y_diff**2))