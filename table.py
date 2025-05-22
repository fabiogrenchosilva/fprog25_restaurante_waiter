'''

Group n.º 29
Elements:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

Version 28: 22-05-2025 - 12h42

This file containes the implementation of Table class

'''

from src.packages.graphics import *
from texture import Texture

class Table(Texture):
    """ Class for each table in the screen """
    def __init__(self, win: GraphWin, p1: tuple, p2: tuple) -> None:
        Texture.__init__(self, "wood_texture", p1, p2)

        self.win = win

        self.visual = Circle(Point(*p1), 10)
        self.visual.setWidth(0)
        self.visual.setFill(color_rgb(0, 255, 0))

        self.draw(win)
    
    def handle_click(self, point: tuple) -> bool:
        """ Check if the screen click it's on self, if True highlight the table """

        p1 = self.getP1()
        p2 = self.getP2()

        if p1.x <= point[0] <= p2.x and p1.y <= point[1] <= p2.y:
            return True
        return False
    
    def highlight(self) -> None:
        """ Visual representation of selecting a table """
        try:
            self.visual.draw(self.win)
        except:
            pass

    def dehighlight(self) -> None:
        """ Dehighlight self """
        self.visual.undraw()