from src.packages.graphics import *
from utils import relative_to_window_coords, win_to_grid_coords, grid_to_win_coords, distance_p2p
from time import time
from collections import deque
import os

WIN_WIDTH = 1000
WIN_HEIGHT = 800

class Waiter(Circle):
    def __init__(self, win: GraphWin, grid):
        self.position = relative_to_window_coords((float(os.environ.get("WAITER_INIT_POS_X")), float(os.environ.get("WAITER_INIT_POS_Y"))))

        Circle.__init__(self, Point(*self.position), 25)

        self.win = win

        self.pos_to_go = []
        self.grid = grid
        self.grid_position = win_to_grid_coords(self.position)

        self.setWidth(1)
        self.setFill(color_rgb(255, 0, 0))


    def move_to(self, point: tuple, table=False):
        end = win_to_grid_coords(point)
        if table:
            end = self.__find_point(point)
        
        path = self.__bfs(self.grid, self.grid_position, end)
        self.pos_to_go = path


    def __find_point(self, point: tuple):
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
    
    def __move_to_point(self, point: tuple, dt: float):
        point = (int(point[0]*10), int(point[1]*8))
        
        dx = point[0] - self.position[0] 
        dy = point[1] - self.position[1]

        self.move(dx, dy)

        self.position = point
        self.grid_position = win_to_grid_coords(point)
    
    def __bfs(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])

        visited = [[False for _ in range(100)] for _ in range(100)]
        parent = [[None for _ in range(100)] for _ in range(100)]
        
        queue = deque()
        queue.append(start)
        rect = Rectangle(Point(*grid_to_win_coords(start)), Point(*grid_to_win_coords((start[0]+1, start[1]+1))))
        rect.setWidth(0)
        rect.setFill(color_rgb(0, 0, 255))
        rect.draw(self.win)

        visited[start[0]][start[1]] = True

        #directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while queue:
            r, c = queue.popleft()

            if (r, c) == end: 
                rect = Rectangle(Point(r*WIN_WIDTH/100, c*WIN_HEIGHT/100), Point((r+1)*WIN_WIDTH/100, (c+1)*WIN_HEIGHT/100))
                rect.setWidth(0)
                rect.setFill(color_rgb(255, 0, 0))
                rect.draw(self.win)
                break

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if not visited[nr][nc] and grid[nr][nc] == 0:
                        visited[nr][nc] = True
                        parent[nr][nc] = (r, c)
                        queue.append((nr, nc))

                        #rect = Rectangle(Point(nr*WIN_WIDTH/100, nc*WIN_HEIGHT/100), Point((nr+1)*WIN_WIDTH/100, (nc+1)*WIN_HEIGHT/100))
                        #rect.setWidth(0)
                        #rect.setFill(color_rgb(0, 255, 0))
                        #rect.draw(self.win)
        
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = parent[curr[0]][curr[1]]
        
        path.reverse()

        for block in path:
            x = block[0]
            y = block[1]
            rect = Rectangle(Point(x*WIN_WIDTH/100, y*WIN_HEIGHT/100), Point((x+1)*WIN_WIDTH/100, (y+1)*WIN_HEIGHT/100))
            rect.setWidth(0)
            rect.setFill(color_rgb(0, 255, 0))
            rect.draw(self.win)
        
        return path

    def update(self, dt):
        if self.pos_to_go:
            self.__move_to_point(self.pos_to_go[0], dt)
        
            self.pos_to_go.pop(0)   


