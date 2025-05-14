'''
Criado por:
    - Duarte Sousa (ist1113879)
    - Fábio Silva (ist1114303)

    - Grupo 46

'''

from src.packages.graphics import *
from table import Table
from utils import relative_to_window_coords, win_to_grid_coords, grid_to_win_coords, distance_p2p
from collections import deque
import os

class Waiter(Circle):
    def __init__(self, win: GraphWin, grid, charging_station_location: tuple, plates_station_location: tuple) -> None:
        self.position = relative_to_window_coords((float(os.environ.get("WAITER_INIT_POS_X")), float(os.environ.get("WAITER_INIT_POS_Y"))))

        Circle.__init__(self, Point(*self.position), int(os.environ.get("WAITER_RADIUS")))
        
        # Code related to indicate the battery level
        self.battery_indicator = Circle(Point(self.position[0]+18, self.position[1]+18), 8)
        self.battery_indicator.setWidth(0)
        self.battery_indicator.setFill(color_rgb(0, 255, 0))
        
        self.battery_level = 1
        self.needs_battery = False

        # Charging and plates location
        self.charging_station_location = charging_station_location
        self.plates_station_location = plates_station_location

        # Initializing variables for the path finding algorithm, in this case breath first search
        self.pos_to_go = []
        self.grid = grid
        self.grid_position = win_to_grid_coords(self.position)

        # Operation Queue and initializing the queue so that the robot goes to the charging dock 
        self.operation_queue = [MoveOperation(self.charging_station_location)]

        # Debug variables
        self.debug_mode = False
        self.__debug_elements = []

        # Setting render proprieties and drawing them to the screen
        self.setWidth(1)
        self.setFill(color_rgb(255, 0, 0))
        self.draw(win)
        self.battery_indicator.draw(win)
        

    def move_to(self, point: tuple, table=None) -> None:
        """ Function that allows the waiter to go to a specific location or table when isn't None """
        end = win_to_grid_coords(point)

        if table:
            end = self.__find_point(point)
        
        path = self.__bfs(self.grid, self.grid_position, end)
        self.pos_to_go = path

    def add_operations(self, operation) -> None:
        self.operation_queue.extend(operation)

    def __find_point(self, point: tuple) -> tuple:
        
        point = win_to_grid_coords(point)

        # Directions for the path finding algorithm, in this case left, right, up, down, left-up, right-up, left-down and right-down
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        
        dist = 4000 # Just a large number
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
    
    def _move_to_point(self, point: tuple) -> None:
        point = grid_to_win_coords(point)
        
        dx = point[0] - self.position[0] 
        dy = point[1] - self.position[1]

        self.move(dx, dy)
        self.battery_indicator.move(dx, dy)
        self.battery_level -= 0.005

        self.position = point
        self.grid_position = win_to_grid_coords(point)
    
    def __bfs(self, grid, start: tuple, end: tuple) -> list:
        """ Implementation of a Breath First Search path finding algorithm """

        # Debug elements, in this case the line the waiter follows
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

        # Directions for the path finding algorithm, in this case left, right, up, down
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
        
        # Render debug elements
        if bool(os.environ.get("DEBUG_MODE")):
            # Render path elements, in this case just a series of lines
            for i in range(len(path)-1):
                x = path[i][0]
                y = path[i][1]
                rect = Line(Point(*grid_to_win_coords((x, y))), Point(*grid_to_win_coords((path[i+1][0], path[i+1][1]))))
                rect.setWidth(2)
                rect.setFill(color_rgb(0, 255, 0))
                self.__debug_elements.append(rect)

            # Render the starting point as a blue circle
            rect = Circle(Point(*grid_to_win_coords(start)), 2)
            rect.setWidth(0)
            rect.setFill(color_rgb(0, 0, 255))
            self.__debug_elements.append(rect)

            # Render the ending point as a red circle
            rect = Circle(Point(*grid_to_win_coords(end)), 2)
            rect.setWidth(0)
            rect.setFill(color_rgb(255, 0, 0))
            self.__debug_elements.append(rect)
            
            # Drawing all debug elements
            for element in self.__debug_elements:
                element.draw(self.win)
            
        return path
    
    def update(self, dt) -> None:
        # Update the operation queue
        if self.operation_queue:
            # Select the first element of the queue
            current_operation = self.operation_queue[0]

            # Update the current operation and check if it's done
            if current_operation.update(self, dt=dt):
                # If done remove from the list
                self.operation_queue.pop(0)
        
        # Battery level
        if self.battery_level <= 0.2 and not self.needs_battery:
            self.battery_indicator.setFill(color_rgb(255, 0, 0))  
            self.operation_queue.insert(1, MoveOperation(self.charging_station_location))
            self.operation_queue.insert(2, WaitOperation(2, charging=True))    
            self.needs_battery = True  
            
        elif self.battery_level <= 0.5:
            self.battery_indicator.setFill(color_rgb(255, 255, 0))
        elif self.battery_level <= 1:
            self.battery_indicator.setFill(color_rgb(0, 255, 0))

class MoveOperation:
    """ Class for a operation about moving the waiter """
    def __init__(self, location: tuple, table: Table = None):
        self.location = location
        self.started = False
        self.table = table
    
    def update(self, waiter: Waiter = None, dt: float = 0) -> bool:
        " Operation update function "
        if not self.started:
            waiter.move_to(self.location, self.table)
            self.started = True

        if waiter.pos_to_go:
            waiter._move_to_point(waiter.pos_to_go[0])
            waiter.pos_to_go.pop(0)
            return False
        else: 
            return True
    
    def __del__(self):
        if isinstance(self.table, Table):
            self.table.dehighlight()

class WaitOperation:
    """ Class for a operation for waiting x seconds or charging the waiter"""
    def __init__(self, duration: float = 0, charging: bool = False):
        self.duration = duration
        self.charging = charging
        self.waiter = None

    def update(self, waiter: Waiter = None, dt: float = 0) -> bool:
        " Operation update function "
        if not self.waiter:
            self.waiter = waiter

        self.duration -= dt
        return self.duration <= 0

    def __del__(self):
        if self.charging:
            self.waiter.battery_level = 1
            self.waiter.needs_battery = False

class DeliveryOperation:
    """ Class for a operation about delivering to a specif table  """
    def __init__(self, location: tuple, table: Table = None):
        # List of hardcoded operations
        self.operation_list = [
            MoveOperation(location, table=True),   # Move to the selected table
            WaitOperation(2),                      # Wait 2 seconds on the table
            MoveOperation((500, 40), table=True),  # Move to the plates dock
            WaitOperation(2),                      # Wait another 2 seconds
            MoveOperation(location, table=table),  # Deliver the plate to the table
            WaitOperation(2)                       # Wait another 2 seconds
        ]
    
    def update(self, waiter: Waiter = None, dt: float = 0) -> bool:
        " Operation update function "
        if self.operation_list:
            current_operation = self.operation_list[0]

            if current_operation.update(waiter, dt):
                self.operation_list.pop(0)
            
            return False
        else:
            return True
