# Grid.py
import pygame, numpy as np, random
from pygame.locals import *
from math import sqrt
import random, string
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pathfinding import astar_hex
from Hexagon import Hexagon
from terrain_types import terrain_types

class Grid:
    def __init__(self, rows, cols, world_size, h_dist_world, v_dist_world):
        self.rows = rows
        self.cols = cols
        self.world_size = world_size
        self.h_dist_world = h_dist_world[0]
        self.v_dist_world = v_dist_world[0]
        self.terrains = np.random.choice(['grassland', 'swamp', 'forest', 'dark forest', 'hills', 'mountains', 'water'], (rows, cols), p=[0.45, 0.02, 0.45, 0.02, 0.02, 0.02, 0.02])
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
        self.name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        self.clicked_pos = [0.0, 0.0, 0.0]
    
    def init_grid(self):
        grid = np.empty((self.rows, self.cols), dtype=object)

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.h_dist_world*2
                y = row * self.v_dist_world*2
                if row % 2 == 0:
                    x += self.h_dist_world
                    y += self.v_dist_world
                elif row % 2 == 1:
                    x += self.h_dist_world*2
                    y += self.v_dist_world
                z = 0.0
                
                thickness = random.uniform(0.01, 0.05)
                terrain = self.terrains[row, col]
                graphic = self.terrain_graphics[terrain]
                hexagon = Hexagon(row=row, col=col, radius=self.world_size, thickness=thickness, terrain=terrain, graphic=graphic, pos=(x, y, z)) # Create a hexagon at the world coordinates
                grid[row, col] = hexagon
        return grid
    
    def select_hexagon(self, clicked_pos):
        selected_hexagon = None
        for row in range(self.rows):
            for col in range(self.cols):
                hexagon = self.grid[row, col]
                if hexagon.contains_point(clicked_pos):
                    selected_hexagon = hexagon
                    print("Clicked on hexagon at ", selected_hexagon.row, selected_hexagon.col)
        return selected_hexagon

    # draw the grid on the screen with hexagons 
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row, col].draw()

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
    
    # Check if a hexagon is inside the grid
    def in_bounds(self, hexagon):
        row, col = hexagon
        return 0 <= row < self.rows and 0 <= col < self.cols
    
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