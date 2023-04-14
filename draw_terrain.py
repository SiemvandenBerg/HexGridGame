# draw_terrain.py

import pygame
import numpy as np
from utils import colors, screen, rows, cols, hex_size, initial_screen_pos
from calculate import game_screen_offset_x, game_screen_offset_y, point_in_hexagon
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types

# This function draws pixelArtSurfaces on the screen at the position of the hex tiles in the grid using the offset values of the hex tiles. 
# The terrain arrays are taken from terrain_arrays folder and stored in a dictionary with the key being the name of the terrain.
# Then the pixelArtSurfaces are generated with the DrawImageFromSquares function.
# The pixelArtSurfaces are stored in a dictionary with the key being the name of the pixelArtSurface.
# Then the pixelArtSurfaces are drawn on the screen at the position of the hex tiles depending on the type of terrain of the hexagon tile in the grid.
# The offset values are calculated in the draw_grid function.

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

def draw_terrain(grid):
    terrain_arrays = {}
    for terrain in terrain_types:
        print(terrain)
        # open the image file with OpenImageFile function and store it in a variable and print it
        terrain_image = OpenImageFile(terrain)
        # from the terrain_image variable, create a pixelArtSurface with the DrawImageFromSquares function and store it in a variable and print it
        terrain_pixelArtSurface = DrawImageFromSquares(terrain_image)

        # print(terrain_image)
        print(terrain_pixelArtSurface)
        print("terrain_pixelArtSurface: ", terrain_pixelArtSurface)

        # store the terrain_pixelArtSurface in a dictionary with the key being the name of the terrain
        terrain_arrays[terrain] = terrain_pixelArtSurface
        # display the terrain_pixelArtSurface on the screen with the blit function at a random position
        screen.blit(terrain_pixelArtSurface, (100, 100))
        # update the screen with the new terrain
        pygame.display.update()

    size = hex_size
    h_dist = size * np.sqrt(3)
    v_dist = size * 3/2
    screen.fill((0, 0, 0))
    for row in range(grid.rows):
        for col in range(grid.columns):
            hexagon = grid.get_hexagon(row, col)
            # center_x, center_y = hex_to_pixel(hexagon)
            # get the center_x and center_y values from the hexagon object
            # center_x = hexagon.center_x

            print("hexagon: ", hexagon)

            # find the position of the hexagon tile on the screen
            if row % 2 == 0:
                center_x = col * h_dist + (size*3)/2
                center_y = row * v_dist + size*2.5
            else:
                center_x = col * h_dist + (size*3)/2 + h_dist/2
                center_y = row * v_dist + size*2.5

            terrain_type = grid.get_terrain(row, col)
            terrain_image = terrain_arrays[terrain_type]
            screen.blit(terrain_image, (center_x, center_y))
        pygame.display.update()
    
    #update the screen with the new terrain