import pygame, numpy as np, ast, sys, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Grid import Grid
from Hexagon import Hexagon
from calculate import point_in_hexagon, update_game_screen_position, game_screen_offset_x, game_screen_offset_y, dx, dy
from pathfinding import astar_hex
from utils import h_dist, v_dist, rows, cols, size, screen_width, screen_height, initial_screen_pos, layer1, initial_screen_pos, layer1

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
start = None
end = None
screenPos = (0, 0)
initial_screen_pos = (0, 0) 

running=True
selected_hexagon = None
right_mouse_down = False
prev_mouse_pos = None

layer1.fill((200, 200, 200))  # Fill layer 1 with grey color

display = (screen_width, screen_height)
# 2D mode currently broken
view_mode = '3d'

while running:
    # 2D mode currently broken
    if view_mode == '2d':
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
                    # get_grid(screenPos, grid)
                    # draw_terrain(grid)
                    pygame.display.update()
                    prev_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    # right mouse button
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
                                    # print('start: {}'.format(start))
                                elif end is None and (row, col) != start:
                                    end = (row, col)
                                    # print('end: {}'.format(end))
                                    # path = astar_hex(grid, start, end)
                                    # get_grid(screenPos, grid)
                                    pygame.display.update()
                                    start = None
                                    end = None

        # Draw grid with initial screen position one time to  initialize layer1
        if initial_screen_pos == (0, 0):
            # draw_hexagons(grid)
            initial_screen_pos = (1, 1)    

        pygame.display.flip()
        pygame.time.wait(1)        

        # draw layer 2 on top of layer 1
        # screen.blit(layer1, layer1_rect)
        # screen.blit(layer2, layer2_rect)

    elif view_mode == '3d':

        h_dist = size * np.sqrt(3)
        v_dist = size * 3/2

        pygame.init()
        display = (1024,768)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        # initialize OpenGL
        glMatrixMode(GL_PROJECTION)
        # fill the screen with white color 
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glLoadIdentity()
        gluPerspective(20, (display[0]/display[1]), 0.1, 500.0) # set the perspective of the camera (fov, aspect ratio, near clipping plane, far clipping plane)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
       
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 1.0, 1.0, 0.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

        glTranslatef(0, 0, -15) 
        glRotatef(-45, 1, 0, 0)

        grid = Grid(rows, cols)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # if arrow keys are pressed, move the camera
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        glTranslatef(0,0.1,0)
                    if event.key == pygame.K_DOWN:
                        glTranslatef(0,-0.1,0)
                    if event.key == pygame.K_LEFT:
                        # rotate the camera 1 degree on the z axis
                        glRotatef(1, 0, 0, 1)
                    if event.key == pygame.K_RIGHT:
                        # rotate the camera 1 degree on the z axis
                        glRotatef(-1, 0, 0, 1)
                # if plus or minus keys are pressed, zoom in or out
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_EQUALS:
                        glTranslatef(0,0,0.1)
                    if event.key == pygame.K_MINUS:
                        glTranslatef(0,0,-0.1)
                    
            glDisable(GL_DEPTH_TEST)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            # draw_hexagons(grid)
            grid.draw_grid()
        
            # rotate the camera 1 degree on the z axis for fancy spinning effect
            # glRotatef(1, 0, 0, 1)

            pygame.display.flip()
            pygame.time.wait(1)        
    else:
        pygame.quit()
pygame.quit()
sys.exit()