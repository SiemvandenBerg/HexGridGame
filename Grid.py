import pygame, numpy as np, random
from pygame.locals import *
from Hexagon import Hexagon
from terrain_types import terrain_types
from utils import h_dist, v_dist, cols, size

# Define the hexgraph class
class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.terrains = np.random.choice(['grassland', 'swamp', 'forest', 'dark forest', 'hills', 'mountains', 'water'], (rows, cols), p=[0.45, 0.02, 0.45, 0.02, 0.02, 0.02, 0.02])
        self.colors = self.init_colors()
        pygame.display.set_caption('Hexagonal Grid')
        self.hexagons = {}
        self.terrain_graphics = {
            'grassland': pygame.image.load('terrain_images/grassland.jpg'),
            'swamp': pygame.image.load('terrain_images/swamp.jpg'),
            'forest': pygame.image.load('terrain_images/forest.jpg'),
            'dark forest': pygame.image.load('terrain_images/dark_forest.jpg'),
            'hills': pygame.image.load('terrain_images/hills.jpg'),
            'mountains': pygame.image.load('terrain_images/mountains.jpg'),
            'water': pygame.image.load('terrain_images/water.jpg')
        }
        self.grid = self.init_grid()

    def get_hexagon(self, row, col):
        """Returns the hexagon at the given row and column"""
        return row, col
    
    def get_terrain(self, row, col):
        """Returns the terrain of the hexagon at the given row and column"""
        return self.terrains[row][col]
    
    # Initialize the colors of the grid to the terrain colors of the grid 
    def init_colors(self):
        colors = np.empty((self.rows, self.columns, 3), dtype=int)
        for row in range(self.rows):
            for col in range(self.columns):
                terrain = self.terrains[row, col]
                colors[row, col] = terrain_types[terrain]['color']
        return colors  
        
    # Initialize the grid with hexagons
    def init_grid(self):
        grid = np.empty((self.rows, self.columns), dtype=object)
        for row in range(self.rows):
            # print("row in init grid: " , row)
            for col in range(self.columns):
                # print("col in init grid: " , col)
                if row % 2 == 0:
                    center_x = col * h_dist + (size*3)/2
                    center_y = row * v_dist + size*2.5
                else:
                    center_x = col * h_dist + (size*3)/2 + h_dist/2
                    center_y = row * v_dist + size*2.5
                # Offset the center of the entire grid to the center of the screen 
                
                print(self.columns * size, self.rows * size)
                
                center_x -= (self.columns * size)
                center_y -= (self.rows * size)

                
                thickness = random.uniform(0.1, 0.5)
                # round thickness to 1 decimal places
                thickness = round(thickness, 1)

                terrain = self.terrains[row, col]
                # print("terrain in init: " , terrain)
                graphic = self.terrain_graphics[terrain]  # Set graphic based on terrain type
                self.hexagons[row, col] = Hexagon(x=center_x, y=center_y, row=row, col=col, radius=size, thickness=thickness, terrain=terrain, graphic=graphic)
        return grid

    # draw the grid on the screen with hexagons 
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.hexagons[row, col].draw()

    # init the terrain images
    def init_terrain_images(self):
        terrain_images = {}
        for terrain_type in terrain_types:
            terrain_type = terrain_type.replace(' ', '_')
            terrain_images[terrain_type] = pygame.image.load(terrain_types[terrain_type]['image'])
        return terrain_images

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
        x = col
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
        center_x = size * np.sqrt(3) * (hexagon[1] + 0.5 * (hexagon[0] % 2))
        center_y = size * 3 / 2 * hexagon[0]
        return (center_x, center_y)

    def add_hexagon(self, hexagon):
        row, col = hexagon.row, hexagon.col
        if row not in self.hexagons:
            self.hexagons[row] = {}
        self.hexagons[row][col] = hexagon