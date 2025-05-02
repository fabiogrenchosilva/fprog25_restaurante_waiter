from src.packages.graphics import *
from utils import relative_to_window_coords, win_to_grid_coords, grid_to_win_coords, distance_p2p
from collections import deque
import os

class Waiter(Circle):
    def __init__(self, win: GraphWin, grid):
        self.position = relative_to_window_coords((float(os.environ.get("WAITER_INIT_POS_X")), float(os.environ.get("WAITER_INIT_POS_Y"))))

        Circle.__init__(self, Point(*self.position), int(os.environ.get("WAITER_RADIUS")))

        self.win = win

        # This is a commentf
        self.pos_to_go = []
        self.grid = grid
        self.grid_position = win_to_grid_coords(self.position)

        # Operation
        self.operation = None

        self.setWidth(1)
        self.setFill(color_rgb(255, 0, 0))

        self.__debug_elements = []


    def move_to(self, point: tuple, table=False) -> None:
        end = win_to_grid_coords(point)
        if table:
            end = self.__find_point(point)
        
        path = self.__bfs(self.grid, self.grid_position, end)
        self.pos_to_go = path


    def __find_point(self, point: tuple) -> tuple:
        point = win_to_grid_coords(point)

        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        
        dist = 4000 #Just a large number
        point_finded = (0, 0)
        for dir in directions:
            x, y = point[0], point[1]
            find = False
            while not find:
                x, y = x+dir[0], y+dir[1]
                if self.grid[x][y] == 0:
                    find = True
                    dist_to_p = distance_p2p((x, y), point)[2]
                    if dist_to_p < dist:
                        dist = dist_to_p
                        point_finded = (x, y)
        
        return point_finded
    
    def __move_to_point(self, point: tuple) -> None:
        point = grid_to_win_coords(point)
        
        dx = point[0] - self.position[0] 
        dy = point[1] - self.position[1]

        self.move(dx, dy)

        self.position = point
        self.grid_position = win_to_grid_coords(point)
    
    def __bfs(self, grid, start: tuple, end: tuple) -> list:
        for element in self.__debug_elements:
            element.undraw()
            del element

        self.__debug_elements = []

        rows, cols = len(grid), len(grid[0])

        visited = [[False for _ in range(100)] for _ in range(100)]
        parent = [[None for _ in range(100)] for _ in range(100)]
        
        queue = deque()
        queue.append(start)

        visited[start[0]][start[1]] = True

        #directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while queue:
            r, c = queue.popleft()

            if (r, c) == end: 
                break

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if not visited[nr][nc] and grid[nr][nc] == 0:
                        visited[nr][nc] = True
                        parent[nr][nc] = (r, c)
                        queue.append((nr, nc))

        
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = parent[curr[0]][curr[1]]
        
        path.reverse()
        
        for i in range(len(path)-1):
            x = path[i][0]
            y = path[i][1]
            rect = Line(Point(*grid_to_win_coords((x, y))), Point(*grid_to_win_coords((path[i+1][0], path[i+1][1]))))
            rect.setWidth(2)
            rect.setFill(color_rgb(0, 255, 0))
            self.__debug_elements.append(rect)


        rect = Circle(Point(*grid_to_win_coords(start)), 2)
        rect.setWidth(0)
        rect.setFill(color_rgb(0, 0, 255))
        self.__debug_elements.append(rect)


        rect = Circle(Point(*grid_to_win_coords(end)), 2)
        rect.setWidth(0)
        rect.setFill(color_rgb(255, 0, 0))
        self.__debug_elements.append(rect)
        
        for element in self.__debug_elements:
            element.draw(self.win)
            
        return path
    
    
    def __debug_mode(self, mode: bool) -> None:
        pass

    def update(self, dt) -> None:
        if self.pos_to_go:
            self.__move_to_point(self.pos_to_go[0])
        
            self.pos_to_go.pop(0)  

        match self.operation:
            case None:
                # return to the dock
                self.move_to((620, 28))
                self.operation = "f"