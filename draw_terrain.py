
import pygame
import pygame.mask
import numpy as np
from utils import screen, hex_size, layer1, layer1_rect, layer2, hex_size
from calculate import game_screen_offset_x, game_screen_offset_y, point_in_hexagon
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types
print(pygame.__version__)

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
terrain_arrays = {}

def get_hexagon_shape(center_x, center_y, hex_size):
    surface = pygame.Surface((hex_size*2, hex_size*2), pygame.SRCALPHA)
    # make the background warm blue
    surface.fill((0, 85, 128))
    points = [
        (hex_size, 0),
        (hex_size*2, hex_size//2),
        (hex_size*2, hex_size*3//2),
        (hex_size, hex_size*2),
        (0, hex_size*3//2),
        (0, hex_size//2)
    ]
    pygame.draw.polygon(surface, (255, 255, 255, 0), points, 0)
    mask = pygame.mask.from_surface(surface)
    mask_rect = mask.get_rect()
    mask_rect.center = (center_x, center_y)
    return surface

def draw_terrain(grid):
    try:
        if not terrain_arrays:
            for terrain in terrain_types:
                try:
                    terrain_image = OpenImageFile(terrain)
                except FileNotFoundError:
                    print(f"Error: {terrain} image file not found.")
                    continue
                terrain_pixelArtSurface = DrawImageFromSquares(terrain_image)
                terrain_arrays[terrain] = terrain_pixelArtSurface
        layer2_rect = layer2.get_rect()
        size = hex_size
        h_dist = size * np.sqrt(3)
        v_dist = size * 3/2
        for row in range(grid.rows):
            for col in range(grid.columns):
                hexagon = grid.get_hexagon(row, col)
                print(hexagon)
                if row % 2 == 0:
                    center_x = col * h_dist + (size*3)/2
                    center_y = row * v_dist + size*2.5
                else:
                    center_x = col * h_dist + (size*3)/2 + h_dist/2
                    center_y = row * v_dist + size*2.5

                center_x -= size
                center_y -= size

                terrain_type = grid.get_terrain(row, col)
                try:
                    terrain_image = terrain_arrays[terrain_type]
                except KeyError:
                    print(f"Error: {terrain_type} terrain not found.")
                    continue
                hexagon_shape = get_hexagon_shape(center_x, center_y, hex_size)
                hexagon_mask = hexagon_shape.convert_alpha()
                print(hexagon_mask.get_alpha())
                mask_rect = hexagon_mask.get_rect()
                mask_rect.center = terrain_image.get_rect().center
                terrain_image = terrain_image.copy()
                terrain_image.blit(hexagon_shape, mask_rect, special_flags=pygame.BLEND_RGBA_MULT)
                layer2.blit(terrain_image, (center_x, center_y))
        screen.blit(layer1, layer1_rect)
        screen.blit(layer2, layer2_rect)
        pygame.display.update()
    except Exception as e:
        print(f"Error: {e}")
