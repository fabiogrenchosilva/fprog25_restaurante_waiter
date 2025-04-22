from src.packages.graphics import *
from time import time
from math import sqrt
from collections import deque

WIN_WIDTH = 1000
WIN_HEIGHT = 800

class Waiter(Circle):
    def __init__(self, win: GraphWin, pos: tuple, grid):
        Circle.__init__(self, Point(*pos), 25)

        self.win = win

        self.current_pos = pos
        self.pos_to_go = []
        self.grid = grid
        self.current_grid_pos = (int(pos[0]/(WIN_WIDTH/10)*10), int(pos[1]/(WIN_HEIGHT/10)*10))

        self.velocity = 200 # px/s

        self.setWidth(1)
        self.setFill(color_rgb(255, 0, 0))

        #self.move_to((40, 60))

    def move_to(self, point: tuple):
        end = (int(point[0]/(WIN_WIDTH/10)*10), int(point[1]/(WIN_HEIGHT/10)*10))
        path = self.__bfs(self.grid, self.current_grid_pos, end)
        self.pos_to_go = path

    
    def __move_to_point(self, point: tuple, dt: float):
        point = (int(point[0]*10), int(point[1]*8))
        x_diff, y_diff, distance = distance_p2p(point, self.current_pos)
        if distance > 2:
            x_norm = x_diff / distance * self.velocity * dt
            y_norm = y_diff / distance * self.velocity * dt

            self.move(x_norm, y_norm)
            self.current_pos = (self.current_pos[0]+x_norm, self.current_pos[1]+y_norm)

            self.current_grid_pos = (int((self.current_pos[0]+x_norm)/(WIN_WIDTH/10)*10), int((self.current_pos[1]+y_norm)/(WIN_HEIGHT/10)*10))

        else:
            self.current_pos = point 
        
        print(self.current_grid_pos, self.current_pos)
    
    def __bfs(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])

        visited = [[False for _ in range(100)] for _ in range(100)]
        parent = [[None for _ in range(100)] for _ in range(100)]
        
        queue = deque()
        queue.append(start)
        rect = Rectangle(Point(start[0]*WIN_WIDTH/100, start[1]*WIN_HEIGHT/100), Point((start[0]+1)*WIN_WIDTH/100, (start[1]+1)*WIN_HEIGHT/100))
        rect.setWidth(0)
        rect.setFill(color_rgb(0, 0, 255))
        rect.draw(self.win)

        visited[start[0]][start[1]] = True

        #directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while queue:
            r, c = queue.popleft()

            if (r, c) == end: 
                print("FOUND IT")
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
            #print(self.pos_to_go)
        
        
    


def distance_p2p(p1: tuple, p2: tuple) -> tuple:
    x_diff = p1[0] - p2[0]
    y_diff = p1[1] - p2[1]
    return (x_diff, y_diff, sqrt(x_diff**2 + y_diff**2))