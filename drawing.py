# drawing.py
import numpy as np
import pygame
from utils import colors, screen, rows, cols, hex_size, initial_screen_pos
from calculate import game_screen_offset_x, game_screen_offset_y
from draw_terrain import draw_terrain
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)

screenPos = (0, 0)

def draw_hexagon(center_x, center_y, size, row, col, colors, in_path):
    global game_screen_offset_x, game_screen_offset_y
    angle = np.pi/6  
    points = []

    for i in range(6):
        x = center_x + size * np.cos(angle)
        y = center_y + size * np.sin(angle)
        points.append([x,y])
        angle += np.pi/3
    
    points.append(points[0])
    
    if in_path:
        color = (255, 0, 0) 
    else:
        color = colors[row, col]

    pygame.draw.polygon(screen, color, points)

    border_color = (0, 85, 128) 
    border_width = 3 
    for i in range(len(points)-1):
        pygame.draw.line(screen, border_color, points[i], points[i+1], border_width)
    
    text = font.render(f"({row}, {col})", True, (0, 0, 0))
    text_rect = text.get_rect(center=(center_x, center_y))
    screen.blit(text, text_rect)

def draw_grid(screenPos):
    global game_screen_offset_x, game_screen_offset_y

    game_screen_offset_x = screenPos[0] 
    game_screen_offset_y = screenPos[1]

    size = hex_size
    h_dist = size * np.sqrt(3)
    v_dist = size * 3/2
    screen.fill((0, 0, 0))

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
            draw_hexagon(center_x=center_x, center_y=center_y, size=size, row=row, col=col, colors=colors, in_path=False)
    
