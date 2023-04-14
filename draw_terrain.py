# draw_terrain.py

import pygame
import numpy as np
from utils import colors, screen, rows, cols, hex_size, initial_screen_pos
from calculate import game_screen_offset_x, game_screen_offset_y
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

# This function draws pixelArtSurfaces on the screen at the position of the hex tiles in the grid using the offset values of the hex tiles. The offset values are calculated in the draw_grid function. The pixelArtSurfaces are generated with the DrawImageFromSquares function. The pixelArtSurfaces are stored in a dictionary with the key being the name of the pixelArtSurface. The pixelArtSurfaces are drawn on the screen at the position of the hex tiles in the grid using the offset values of the hex tiles. The offset values are calculated in the draw_grid function. The pixelArtSurfaces are generated with the DrawImageFromSquares function. The pixelArtSurfaces are stored in a dictionary with the key being the name of the pixelArtSurface. The type of pixelArtSurface is depending on the terrain type of the hexagon tile in the grid.

# Generate the pixelArtSurfaces for the different terrain types.
pixelArtSurfaces = {}
for terrain_type in terrain_types:
    # The pixelArtSurfaces are stored in a dictionary with the key being the name of the pixelArtSurface
    # The type of pixelArtSurface is depending on the terrain type of the hexagon tile in the grid.
    print("in terrain_type for each loop: " + terrain_type)
    OpenImageFile(terrain_type)
    # DrawImageFromSquares
    # pixelArtSurfaces[terrain_type] = 
    # DrawImageFromSquares(terrain_types[terrain_type]["image"], terrain_types[terrain_type]["size"], terrain_types[terrain_type]["size"])

# function that can call the for loop above from the main file
def draw_terrain(screen, pixelArtSurfaces, terrain_types, grid, hex_size, initial_screen_pos):
    global game_screen_offset_x, game_screen_offset_y
    print("in draw_terrain function")
    print(pixelArtSurfaces)

    # size = hex_size
    # h_dist = size * np.sqrt(3)
    # v_dist = size * 3/2
    # screen.fill((0, 0, 0))

    # for row in range(rows):
    #     for col in range(cols):
    #         if row % 2 == 0:
    #             center_x = col * h_dist + (size*3)/2
    #             center_y = row * v_dist + size*2.5
    #         else:
    #             center_x = col * h_dist + (size*3)/2 + h_dist/2
    #             center_y = row * v_dist + size*2.5
    #         center_x -= game_screen_offset_x
    #         center_y -= game_screen_offset_y

    #         # The pixelArtSurfaces are drawn on the screen at the position of the hex tiles in the grid using the offset values of the hex tiles
    #         screen.blit(pixelArtSurfaces[colors[row, col]], (center_x, center_y))
