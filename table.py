'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''
###
### File containing Table class
###

from src.packages.graphics import *
from utils import generate_texture

class Table(Rectangle):
    " Class for each table in the screen "
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple):
        Rectangle.__init__(self, Point(*p1), Point(*p2))

        texture = generate_texture("wood_texture", p1, p2)
        texture.draw(win)
        
        # Render with specifc properties
        self.setWidth(0)
        self.setFill(color_rgb(25, 25, 225))
        #self.draw(win)
    
    def clicked(self, point: tuple) -> bool:
        " Check if the screen click it's on self, if True highlight the table  "

        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            return True
        return False
    
    def highlight(self):
        self.setWidth(5)
        self.setFill(color_rgb(50, 50, 225))

    def dehighlight(self):
        " Dehighlight self "

        self.setWidth(0)
        self.setFill(color_rgb(25, 25, 225))