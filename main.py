# main.py
# from OpenGL.GL import *
# from OpenGL.GLU import *
import pygame, numpy as np, ast, sys, random
# from pygame.locals import *
from hexagongraph import HexagonGraph
from calculate import point_in_hexagon, update_game_screen_position, game_screen_offset_x, game_screen_offset_y, dx, dy
from pathfinding import astar_hex
from drawing import draw_grid
from utils import colors, screen_width, screen_height, rows, cols, hex_size, layer1, layer2, layer1_rect, layer2_rect  
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
terrains = np.random.choice(['grassland', 'swamp', 'forest', 'dark forest', 'hills', 'mountains', 'water'], (rows, cols), p=[0.45, 0.02, 0.45, 0.02, 0.02, 0.02, 0.02])
start = None
end = None
screenPos = (0, 0)
initial_screen_pos = (0, 0) 

grid = HexagonGraph(rows, cols, terrains, colors)
grid.init_colors()

running=True
selected_hexagon = None
right_mouse_down = False
prev_mouse_pos = None

# CAMERA_HEIGHT = 500

# def resize(width, height):
#     glViewport(0, 0, width, height)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(60.0, float(width)/height, .1, 1000.)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# def init():
#     glEnable(GL_DEPTH_TEST)

# def render():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

layer1.fill((200, 200, 200))  # Fill layer 1 with grey color

# pygame.init()
# screen = pygame.display.set_mode((screen_width,screen_height), OPENGL|DOUBLEBUF)
# resize(screen_width,screen_height)
# init()
# clock = pygame.time.Clock()


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
                draw_grid(screenPos, grid)
                # draw_terrain(grid)
                pygame.display.update()
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
                                draw_grid(screenPos, grid)
                                pygame.display.update()
                                start = None
                                end = None
    
    # Draw grid with initial screen position one time to  initialize layer1
    if initial_screen_pos == (0, 0):
        draw_grid(initial_screen_pos, grid)
        # draw_terrain(grid)

        initial_screen_pos = (1, 1)    

    # render()
    pygame.display.flip()

    # draw layer 2 on top of layer 1
    # screen.blit(layer1, layer1_rect)
    # screen.blit(layer2, layer2_rect)
    
pygame.quit()
sys.exit()