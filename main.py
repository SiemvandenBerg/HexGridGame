# main.py
import pygame, numpy as np, ast, sys, random
from hexagongraph import HexagonGraph
from calculate import point_in_hexagon, update_game_screen_position, game_screen_offset_x, game_screen_offset_y, dx, dy
from pathfinding import astar_hex
from drawing import draw_grid
from draw_terrain import draw_terrain
from utils import colors, screen, rows, cols, hex_size
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
pygame.init()
white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
terrains = np.random.choice(['grassland', 'swamp', 'forest', 'dark forest', 'hills', 'mountains', 'water'], (rows, cols), p=[0.7, 0.01, 0.13, 0.13, 0.01, 0.01, 0.01])
start = None
end = None
screenPos = (0, 0)
initial_screen_pos = (0, 0) 

def display_offset_info():
    global game_screen_offset_x, game_screen_offset_y
    info_box_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    info_box_rect = pygame.Rect(20, 20, 200, 50)
    pygame.draw.rect(screen, info_box_color, info_box_rect)
    offset_info_str = f"Info Offset: ({game_screen_offset_x}, {game_screen_offset_y})"
    offset_info_text = font.render(offset_info_str, None, (0, 0, 0))
    offset_info_rect = offset_info_text.get_rect(center=info_box_rect.center)
    screen.blit(offset_info_text, offset_info_rect)

grid = HexagonGraph(rows, cols, terrains, colors)
grid.init_colors()
    
running=True
selected_hexagon = None
right_mouse_down = False
prev_mouse_pos = None

screen.fill(black)
draw_grid(initial_screen_pos)
draw_terrain(grid)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                right_mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if right_mouse_down:
                delta_x = event.pos[0] - prev_mouse_pos[0]
                delta_y = event.pos[1] - prev_mouse_pos[1]
                screenPos = update_game_screen_position(delta_x, delta_y, screenPos)
                draw_grid(screenPos)
                prev_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                # right mouse button
                print('right mouse button')
                right_mouse_down = True
                prev_mouse_pos = event.pos
                mouse_x, mouse_y = event.pos
                mouse_x -= game_screen_offset_x + screenPos[0]
                mouse_y -= game_screen_offset_y + screenPos[1]
            if event.button == 1:
                # left mouse button
                mouse_x, mouse_y = event.pos
                mouse_x += game_screen_offset_x + screenPos[0]
                mouse_y += game_screen_offset_y + screenPos[1]
                size = hex_size
                h_dist = size * np.sqrt(3)
                v_dist = size * 3/2
                selected_hexagon = None
                for row in range(rows):
                    for col in range(cols):
                        if row % 2 == 0:
                            center_x = col * h_dist + (size*3)/2
                            center_y = row * v_dist + size*2.5
                        else:
                            center_x = col * h_dist + (size*3)/2 + h_dist/2
                            center_y = row * v_dist + size*2.5
                        if point_in_hexagon(mouse_x, mouse_y, center_x, center_y, size, game_screen_offset_x, game_screen_offset_y):

                            if start is None:
                                start = (row, col)
                                print('start: {}'.format(start))
                            elif end is None and (row, col) != start:
                                end = (row, col)
                                print('end: {}'.format(end))
                                path = astar_hex(grid, start, end)
                                start = None
                                end = None
                                draw_grid(initial_screen_pos)

    # Draw the grid once per frame
    # draw_grid(screenPos)

    pygame.display.flip()
pygame.quit()
sys.exit()