'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *
from table import Table
from obstacle import Obstacle
from dock import Dock
from waiter import Waiter
import time

WIN_WIDTH = 1000
WIN_HEIGHT = 800

class Window(GraphWin):
    def __init__(self):
        GraphWin.__init__(self, "FProg", WIN_WIDTH, WIN_HEIGHT)

        # Load/generate static objects
        self.tables = []
        self.obstacles = []
        self.docks = []

        self.tables, self.obstacles, self.pratos, self.docks = self.load_file("src/salas/sala01.txt")
        self.generate_room()

        # Load waiter class
        self.waiter = Waiter(self, self.relative_to_window_coords((0.5, 0.5)))
        self.waiter.draw(self)

        """
        for i in range(100):
            for j in range(100):
                Rectangle(Point(i*WIN_WIDTH/100, j*WIN_HEIGHT/100), Point((i+1)*WIN_WIDTH/100, (j+1)*WIN_HEIGHT/100)).draw(self)"""
        
        self.restaurant_grid = [[0 for _ in range(100)] for _ in range(100)]

        p1 = (19, 20)
        p2 = (999, 500)

        for i in range(int(p1[0]/100*10), int(p2[0]/100*10)+1):
            for j in range(int(p1[1]/100*10), int(p2[1]/100*10)+1):
                self.restaurant_grid[i][j] = 1
        
        for i in range(100):
            for j in range(100):
                if self.restaurant_grid[i][j] == 1:
                    rect = Rectangle(Point(i*WIN_WIDTH/100, j*WIN_HEIGHT/100), Point((i+1)*WIN_WIDTH/100, (j+1)*WIN_HEIGHT/100))
                    rect.setFill(color_rgb(0, 0, 0))
                    rect.draw(self)
                else:
                    rect = Rectangle(Point(i*WIN_WIDTH/100, j*WIN_HEIGHT/100), Point((i+1)*WIN_WIDTH/100, (j+1)*WIN_HEIGHT/100))
                    rect.setWidth(0)
                    rect.draw(self)

    
    # Function to change relative coords to window coords
    def relative_to_window_coords(self, point) -> tuple:
        x_pos = point[0] * WIN_WIDTH
        y_pos = point[1] * WIN_HEIGHT

        return (x_pos, y_pos)
    
    def load_file(self, ficheiro_sala: str) -> tuple:
        file = open(ficheiro_sala, 'r')

        tables = []
        obstacles = []
        docks = []

        for line in file:
            line.strip()        
            if not (line.startswith("#") or line.startswith("\n")):
                elements = line.split(" ")

                coords = []

                for i in range(1, len(elements)):
                    coords.append(float(eval(elements[i])))

                x_rel, y_rel, width, height = coords[0], coords[1], coords[2], coords[3]

                p1 = self.relative_to_window_coords((x_rel, y_rel))
                p2 = self.relative_to_window_coords((x_rel + width, y_rel + height))

                match elements[0]:
                    case "Table":            
                        table = Table(self, p1, p2)
                        tables.append(table)
                    
                    case "Obstacle":
                        obstacle = Obstacle(self, p1, p2)
                        obstacles.append(obstacle)

                    case "Dock":
                        dock = Dock(self, p1, p2)
                        docks.append(dock)

                    case "Pratos":
                        pratos = Dock(self, p1, p2)
                    
                    case _:
                        raise ValueError(f'Elemento "{elements[0]}" em "{ficheiro_sala}" desconhecido')

        return (tables, obstacles, pratos, docks)
            
    def generate_room(self) -> None:
        for table in self.tables:
            table.draw(self)

        for obstacle in self.obstacles:
            obstacle.draw(self)

        for dock in self.docks:
            dock.draw(self)

        self.pratos.draw(self)

    def check_colision(self):
        pass

    def main_loop(self) -> bool:
        last_time = time.time()
        while True:
            try:
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time

                key = self.checkKey()
                po = self.checkMouse()
                if po:
                    self.waiter.move_to((po.x, po.y))
                if key:
                    self.waiter.Move(key)
                    print(key)
                

                if self.isClosed():
                    break
                self.waiter.update(dt)
                update(60)

            except GraphicsError:
                break

        return True


def main():
    win = Window()

    win.main_loop()

if __name__=='__main__':
    main()


