# main.py
import pygame, numpy as np, random
from pygame.locals import *
from math import sqrt
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Grid import Grid
from utils import *
from pathfinding import astar_hex

ui_surface = pygame.Surface((display[0], display[1]), pygame.SRCALPHA)
grid = Grid(rows, cols, world_size, world_h_dist, world_v_dist)
start = None
end = None

def handle_events():
    global running, last_clicked_pos, start, end
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = (mouse_pos[0], screen_height - mouse_pos[1])         
                depth_value = glReadPixels(mouse_pos[0], mouse_pos[1], 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)       
                mouse_pos = gluUnProject(mouse_pos[0], mouse_pos[1], depth_value, modelview, projection, viewport)
                last_clicked_pos = mouse_pos
                selected_hex = grid.select_hexagon(mouse_pos)
                print('selected_hex: {}'.format(selected_hex))
                if selected_hex:
                    if start is None:
                        start = (selected_hex.row, selected_hex.col)
                        print('start: {}'.format(start))
                    elif end is None and (selected_hex.row, selected_hex.col) != start:
                        end = (selected_hex.row, selected_hex.col)
                        print('end: {}'.format(end))
                        path = astar_hex(grid, start, end)
                        print('path: {}'.format(path))
                        start = None
                        end = None

def main():
    ui_surface = pygame.Surface((display[0], display[1]), pygame.SRCALPHA)
    clock = pygame.time.Clock()

    while True:
        handle_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        grid.draw_grid()
        glDisable(GL_DEPTH_TEST)

        ui_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(ui_surface, (255, 0, 0), (0, 0, 50, 50))
        screen.blit(ui_surface, (0, 0))
        pygame.display.flip()
        clock.tick(60)

main()