from src.packages.graphics import *

class Waiter():
    def __init__(self, win: GraphWin, position: tuple):

        self.rectangle = Circle(Point(*position), 20)
        self.win = win

        self.rectangle.setWidth(1)
        self.rectangle.setFill(color_rgb(255, 0, 0))

    def draw(self):
        self.rectangle.draw(self.win)

    def undraw(self):
        self.rectangle.undraw(self.win)
    
    def move(self, key):
        match key:
            case "w":
                self.rectangle.move(0, -10)
            case "a":
                self.rectangle.move(-10, 0)
            case "s":
                self.rectangle.move(0, 10)
            case "d":
                self.rectangle.move(10, 0)