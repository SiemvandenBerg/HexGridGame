# hexagon_graph.py
from terrain_types import terrain_types
from utils import hex_size
import numpy as np

# Define the hexgraph class
class Grid:
    def __init__(self, rows, columns, terrains, colors):
        self.rows = rows
        self.columns = columns
        self.terrains = np.array(terrains)  # Convert to NumPy array
        self.colors = colors
        self.hexagons = {}

    def get_hexagon(self, row, col):
        """Returns the hexagon at the given row and column"""
        return row, col
    
    def get_terrain(self, row, col):
        """Returns the terrain of the hexagon at the given row and column"""
        return self.terrains[row][col]

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
    
    def heuristic_cost_estimate(self, start, goal):
        start_cube = self.hex_to_cube(start)
        goal_cube = self.hex_to_cube(goal)
        return self.hex_cube_distance(start_cube, goal_cube)
    
    def hex_cost(self, current, neighbor):
        
        row, col = current
        n_row, n_col = neighbor
        terrain_type = terrain_types[self.terrains[n_row, n_col]]
        return terrain_type['movement_cost']
    
    def hex_to_cube(self, hexagon):
        row, col = hexagon
        x = col,
        z = row
        y = -x - z
        return (x, y, z) 
    
    # Calculate the distance between two hexagons using cube distance
    def hex_cube_distance(self, a, b):
        if len(a) != 3 or len(b) != 3:
            raise ValueError("hex_distance() takes 2 hexagon cube coordinates as input")
        x1, y1, z1 = a
        x2, y2, z2 = b
        distance = max(abs(x1-x2), abs(y1-y2), abs(z1-z2))
        return (distance + 1) // 2
    
    # Draw a path on the grid by changing the color of the hexagons in the path
    def draw_path(self, path):
        for hexagon in path:
            row, col = hexagon
            self.colors[row][col] = (255, 0, 0)

    def hex_to_pixel(self, hexagon):
        # print("Hex to pixel")
        center_x = hex_size * np.sqrt(3) * (hexagon[1] + 0.5 * (hexagon[0] % 2))
        center_y = hex_size * 3 / 2 * hexagon[0]
        return (center_x, center_y)

    def hex_to_3d(self, hexagon):
        # print("Hex to 3D")
        center_x, center_y = self.hex_to_pixel(hexagon)
        center_z = 0
        x = center_x
        y = center_y
        z = center_z
        return np.dot(np.array([[np.sqrt(3), 0, 0], [np.sqrt(3)/2, 3/2, 0], [0, 0, -1/2]]), np.array([x, y, z]))

    def convert_to_3d(self, center):
        # print("Converting to 3D")
        center_x, center_y = center
        x = center_x
        y = center_y
        z = -x - y
        return np.dot(np.array([[np.sqrt(3), 0, 0], [np.sqrt(3)/2, 3/2, 0], [0, 0, -1/2]]), np.array([x, y, z]))

    def add_hexagon(self, hexagon):
        print("Adding hexagon at row: {}, col: {}".format(hexagon.row, hexagon.col))
        row, col = hexagon.row, hexagon.col
        if row not in self.hexagons:
            self.hexagons[row] = {}
        # print("Hexagon row: {}".format(hexagon.row))
        print(type(hexagon))

        self.hexagons[row][col] = hexagon
        # print(self.hexagons)
        # hexagon.set_3d_coords(self)