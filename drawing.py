# drawing.py
import numpy as np
import pygame
import pygame.mask
from utils import rows, cols, hex_size, layer2
from calculate import game_screen_offset_x, game_screen_offset_y
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
screenPos = (0, 0)

def get_points(center_x, center_y, size):
    points = []
    angle = np.pi/6  
    for i in range(6):
        x = center_x + size * np.cos(angle)
        y = center_y + size * np.sin(angle)
        points.append([x,y])
        angle += np.pi/3
    points.append(points[0])
    return points

def draw_hexagon(center_x, center_y, size, row, col, layer, grid):
    terrain_type = grid.get_terrain(row, col)
    draw_terrain_graphic(center_x, center_y, size, row, col, terrain_type, layer)
    draw_hexagon_border(center_x, center_y, size, row, col, layer)

def draw_hexagon_border(center_x, center_y, size, row, col, layer):
    points = get_points(center_x, center_y, size)
    border_color = (0, 85, 128) 
    border_width = 3 
    for i in range(len(points)-1):
        pygame.draw.line(layer, border_color, points[i], points[i+1], border_width)
    text = font.render(f"({row}, {col})", True, (255, 255, 255))
    text_rect = text.get_rect(center=(center_x, center_y))
    layer.blit(text, text_rect)


def get_hexagon_shape(center_x, center_y, size):
    surface = pygame.Surface(size=(hex_size*2, hex_size*2), flags=pygame.SRCALPHA)    
    points = get_points(center_x, center_y, size)
    pygame.draw.polygon(surface=surface, color=(255, 255, 255, 255), points=points)
    return surface 

def get_terrain_images(terrain_types):
    terrain_images = {}
    for terrain in terrain_types:
        image = OpenImageFile(terrain)
        image = DrawImageFromSquares(image)
        terrain_images[terrain] = image
    return terrain_images
terrain_images = get_terrain_images(terrain_types)

def draw_terrain_graphic(center_x, center_y, hex_size, row, col, terrain_type, layer):
    terrain_image = terrain_images[terrain_type]
    hex = get_hexagon_shape(center_x=60, center_y=60, size=hex_size)
    image = pygame.transform.scale(terrain_image, (hex_size*2, hex_size*2))
    # Create a new surface with the same size as the image surface and an alpha channel
    clipped_image = pygame.Surface((hex_size*2, hex_size*2), flags=pygame.SRCALPHA)
    # Blit the image surface onto the new surface
    clipped_image.blit(image, (0, 0))
    # Blit the hex surface onto the new surface with the BLEND_RGBA_MULT flag
    clipped_image.blit(hex, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    # Blit the clipped image surface onto the layer
    layer.blit(clipped_image, (center_x-hex_size, center_y-hex_size))

def draw_grid(screenPos, grid):
    global game_screen_offset_x, game_screen_offset_y

    game_screen_offset_x = screenPos[0] 
    game_screen_offset_y = screenPos[1]

    size = hex_size
    h_dist = size * np.sqrt(3)
    v_dist = size * 3/2

    # clear the layer
    layer2.fill((0, 0, 0, 0))

    for row in range(rows):
        for col in range(cols):
            if row % 2 == 0:
                center_x = col * h_dist + (size*3)/2
                center_y = row * v_dist + size*2.5
            else:
                center_x = col * h_dist + (size*3)/2 + h_dist/2
                center_y = row * v_dist + size*2.5
            center_x -= game_screen_offset_x
            center_y -= game_screen_offset_y
            draw_hexagon(center_x=center_x, center_y=center_y, size=size, row=row, col=col, layer=layer2, grid=grid)