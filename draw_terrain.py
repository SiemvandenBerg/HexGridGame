# draw_terrain.py
# This function draws pixelArtSurfaces on the screen at the position of the hex tiles in the grid using the offset values of the hex tiles. 
# The terrain arrays are taken from terrain_arrays folder and stored in a dictionary with the key being the name of the terrain.
# Then the pixelArtSurfaces are generated with the DrawImageFromSquares function.
# The pixelArtSurfaces are stored in a dictionary with the key being the name of the pixelArtSurface.
# Then the pixelArtSurfaces are drawn on the screen at the position of the hex tiles depending on the type of terrain of the hexagon tile in the grid.
# The offset values are calculated in the draw_grid function.
# draw_terrain.py

import pygame
import numpy as np
from utils import colors, screen, rows, cols, hex_size, initial_screen_pos, layer1, layer1_rect, layer2, layer2_rect
from calculate import game_screen_offset_x, game_screen_offset_y, point_in_hexagon
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
terrain_arrays = {}

def draw_terrain(grid):
    # if terrain_arrays is empty, then fill it with the terrain arrays
    if not terrain_arrays:
        for terrain in terrain_types:
            # open the image file with OpenImageFile function and store it in a variable
            terrain_image = OpenImageFile(terrain)
            # from the terrain_image variable, create a pixelArtSurface with the DrawImageFromSquares function and store it in a variable
            terrain_pixelArtSurface = DrawImageFromSquares(terrain_image)
            # store the terrain_pixelArtSurface in a dictionary with the key being the name of the terrain
            terrain_arrays[terrain] = terrain_pixelArtSurface

    # create layer 2
    layer2_rect = layer2.get_rect()

    size = hex_size
    h_dist = size * np.sqrt(3)
    v_dist = size * 3/2
    for row in range(grid.rows):
        for col in range(grid.columns):
            hexagon = grid.get_hexagon(row, col)

            # find the position of the hexagon tile on the screen
            if row % 2 == 0:
                center_x = col * h_dist + (size*3)/2
                center_y = row * v_dist + size*2.5
            else:
                center_x = col * h_dist + (size*3)/2 + h_dist/2
                center_y = row * v_dist + size*2.5

            terrain_type = grid.get_terrain(row, col)
            terrain_image = terrain_arrays[terrain_type]

            # draw the terrain image on layer 2
            layer2.blit(terrain_image, (center_x, center_y))

    # draw layer 2 on top of layer 1
    screen.blit(layer1, layer1_rect)
    screen.blit(layer2, layer2_rect)

    # update the screen
    pygame.display.update()
