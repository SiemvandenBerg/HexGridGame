# Grid.py
import pygame, numpy as np, random
from pygame.locals import *
from math import sqrt
import random, string
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pathfinding import astar_hex
from terrain_types import terrain_types
from Hexagon import Hexagon
import math

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
                # z = center_of_world[2]
                # offset the center with half the distance between the hexagons
                if row % 2 == 0:
                    x += self.h_dist_world
                    y += self.v_dist_world
                elif row % 2 == 1:
                    x += self.h_dist_world*2
                    y += self.v_dist_world
                z = 0.0
                
                print("Init hex:", row, ",", col, " at pos:", x, y, z)
                
                thickness = random.uniform(0.01, 0.05)
                # thickness = 0.1
                terrain = self.terrains[row, col]
                graphic = self.terrain_graphics[terrain]
                hexagon = Hexagon(row=row, col=col, radius=self.world_size, thickness=thickness, terrain=terrain, graphic=graphic, pos=(x, y, z)) # Create a hexagon at the world coordinates
                grid[row, col] = hexagon
        return grid
    
    def select_hexagon(self, clicked_pos):
        # print("Clicked on ", clicked_pos)
        for row in range(self.rows):
            for col in range(self.cols):
                # print("Checking hexagon at ", row, col)
                hexagon = self.grid[row, col]
                # hexagon.clicked_pos_marker(clicked_pos)
                if hexagon.contains_point(clicked_pos):
                    selected_hexagon = hexagon
                    print("!!! Clicked on hexagon at ", selected_hexagon.row, selected_hexagon.col)
        return None

    # draw the grid on the screen with hexagons 
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # print("drawing hex at ", row, col, self.grid[row, col].pos)
            
                self.grid[row, col].draw()
