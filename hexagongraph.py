# hexagon_graph.py
from terrain_types import terrain_types
from utils import hex_size
import numpy as np

# Define the hexgraph class
class HexagonGraph:
    def __init__(self, rows, columns, terrains, colors):
        self.rows = rows
        self.columns = columns
        self.terrains = np.array(terrains)  # Convert to NumPy array
        self.colors = colors

    def get_hexagon(self, row, col):
        """Returns the hexagon at the given row and column"""
        return row, col
    
    def get_terrain(self, row, col):
        """Returns the terrain of the hexagon at the given row and column"""
        return self.terrains[row][col]
    
    def get_center(self, row, col):
        """Returns the center of the hexagon"""
        size = hex_size
        h_dist = size * np.sqrt(3)
        v_dist = size * 3/2
        if row % 2 == 0:
            center_x = col * h_dist + (size*3)/2
            center_y = row * v_dist + size
        else:
            center_x = col * h_dist + size
            center_y = row * v_dist + size
        return center_x, center_y

    # Initialize the colors of the grid to the terrain colors of the grid 
    def init_colors(self):
        for row in range(self.rows):
            for col in range(self.columns):
                terrain_type = terrain_types[self.terrains[row, col]]
                self.colors[row, col] = terrain_type['color']

    # Check if a hexagon is inside the grid
    def in_bounds(self, hexagon):
        row, col = hexagon
        return 0 <= row < self.rows and 0 <= col < self.columns

    def neighbors_hex(self, hexagon):
        row, col = hexagon
        if row % 2 == 0:
            result = [
                (row - 1, col - 1),
                (row - 1, col),
                (row, col + 1),
                (row + 1, col),
                (row + 1, col - 1),
                (row, col - 1),
            ]
        else:
            result = [
                (row - 1, col),
                (row - 1, col + 1),
                (row, col + 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row, col - 1),
            ]
        result = filter(self.in_bounds, result)
        return result
    
    # Calculate the distance between the start and goal hexagons
    def heuristic_cost_estimate(self, start, goal):
        start_cube = self.hex_to_cube(start)
        goal_cube = self.hex_to_cube(goal)
        return self.hex_cube_distance(start_cube, goal_cube)
    
    # Calculate the distance between the start and goal hexagons using Manhattan distance
    def heuristicManhattan_cost_estimate(self, start, goal):
        start_cube = self.hex_to_cube(start)
        goal_cube = self.hex_to_cube(goal)
        return sum(abs(a - b) for a, b in zip(start_cube, goal_cube))

    # Calculate the cost of moving from one hexagon to another
    def hex_cost(self, current, neighbor):
        row, col = current
        n_row, n_col = neighbor
        terrain_type = terrain_types[self.terrains[n_row, n_col]]
        return terrain_type['movement_cost']
    
    # Generate cube coordinates from axial coordinates
    def hex_to_cube(self, hexagon):
        row, col = hexagon
        x = col
        z = row
        y = -x - z
        return (x, y, z) 

    # Calculate the distance between two hexagons using cube distance
    def hex_cube_distance(self, a, b):
        # If the terrain is not passable, return a high cost
        if len(a) != 3 or len(b) != 3:
            # // Code to follow
            raise ValueError("hex_distance() takes 2 hexagon cube coordinates as input")
        x1, y1, z1 = a
        x2, y2, z2 = b
        # Calculate the cube distance between the two hexagons
        distance = max(abs(x1-x2), abs(y1-y2), abs(z1-z2))
        # Divide the cube distance by 2, rounded up to the nearest integer
        return (distance + 1) // 2

    # Draw a path on the grid by changing the color of the hexagons in the path
    def draw_path(self, path):
        for hexagon in path:
            row, col = hexagon
            self.colors[row][col] = (255, 0, 0)
    