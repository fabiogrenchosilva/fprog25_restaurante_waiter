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
from utils import load_configs, relative_to_window_coords, win_to_grid_coords, grid_to_win_coords
import time, os


class Window(GraphWin):
    def __init__(self):
        GraphWin.__init__(self, "FProg", os.environ.get("WIN_WIDTH"), os.environ.get("WIN_HEIGHT"))

        # Load/generate static objects
        self.tables = []
        self.obstacles = []
        self.docks = []
        self.pratos = None

        self.restaurant_grid = [[0 for _ in range(100)] for _ in range(100)]

        self.__load_file("src/salas/sala01.txt")
        self.__generate_room()

        # Load waiter class
        self.waiter = Waiter(self, self.restaurant_grid)
        self.waiter.draw(self)

        # Debug mode
        self.debug_mode = False
        self.debug_elements = []
    
    
    def __set_grid(self, p1: tuple, p2: tuple):
        point_1, point_2 = win_to_grid_coords(p1), win_to_grid_coords(p2)

        for i in range(point_1[0], point_2[0]+1):
            for j in range(point_1[1], point_2[1]+1):
                self.restaurant_grid[i][j] = 1
    
    
    def __load_file(self, ficheiro_sala: str) -> None:
        file = open(ficheiro_sala, 'r')

        tables = []
        obstacles = []
        docks = []

        for line in file:
            line.strip()     
            if not (line.startswith("#") or line.startswith("\n") or line.startswith("*")):
                elements = line.split(" ")

                coords = []

                for i in range(1, len(elements)):
                    coords.append(float(eval(elements[i])))

                x_rel, y_rel, width, height = coords[0], coords[1], coords[2], coords[3]

                p1 = relative_to_window_coords((x_rel, y_rel))
                p2 = relative_to_window_coords((x_rel + width, y_rel + height))

                match elements[0]:
                    case "Table":            
                        table = Table(self, p1, p2)
                        self.tables.append(table)
                        self.__set_grid((p1[0]-25, p1[1]-25), (p2[0]+25, p2[1]+25))

                    case "Obstacle":
                        obstacle = Obstacle(self, p1, p2)
                        self.obstacles.append(obstacle)
                        self.__set_grid((p1[0]-25, p1[1]-25), (p2[0]+25, p2[1]+25))

                    case "Dock":
                        dock = Dock(self, p1, p2)
                        self.docks.append(dock)

                    case "Pratos":
                        self.pratos = Dock(self, p1, p2)
                    
                    case _:
                        raise ValueError(f'Elemento "{elements[0]}" em "{ficheiro_sala}" desconhecido')
                    
        file.close()

            
    def __generate_room(self) -> None:
        for table in self.tables:
            table.draw(self)

        for obstacle in self.obstacles:
            obstacle.draw(self)

        for dock in self.docks:
            dock.draw(self)

        self.pratos.draw(self)

   
    def __debug_mode(self) -> None:
        self.debug_mode = not self.debug_mode
        os.environ["DEBUG_MODE"] = str(self.debug_mode)
        print(f"Debug mode was setted to: {self.debug_mode}")
       
        for element in self.debug_elements:
            element.undraw()
            del element

        if self.debug_mode:
            for i in range(100):
                for j in range(100):
                    if self.restaurant_grid[i][j] == 1:
                        rect = Rectangle(Point(*grid_to_win_coords((i, j))), Point(*grid_to_win_coords((i+1, j+1))))
                        rect.draw(self)
                        self.debug_elements.append(rect)


    def __click_handler(self) -> None:
        clicked_point = self.checkMouse()
        if not clicked_point:
            return
        
        for table in self.tables:
            if table.clicked((clicked_point.x, clicked_point.y)):
                self.waiter.move_to((clicked_point.x, clicked_point.y), table=True)
                return True
        
        self.waiter.move_to((clicked_point.x, clicked_point.y))

  
    def __key_handler(self) -> None:
        pass


    def main_loop(self) -> bool:
        last_time = time.time()
        while True:
            try:
                ####################
                ## Delta time code #
                ####################
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time
                ####################

                key = self.checkKey()    

                self.__click_handler()
                if key == "F12":
                    self.__debug_mode()
                

                if self.isClosed():
                    break
                self.waiter.update(dt)
                update(60)

            except GraphicsError as err:
                print(err)
                break

        return True


def main():
    win = Window()

    win.main_loop()


if __name__=='__main__':
    main()


