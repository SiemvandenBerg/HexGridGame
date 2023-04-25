# main.py
import pygame, numpy as np, random
from pygame.locals import *
from math import sqrt
import random, string
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Grid import Grid
from Hexagon import Hexagon
from utils import *

def handle_events():
    global running, last_clicked_pos
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
                # print("mouse pos", mouse_pos)
                last_clicked_pos = mouse_pos
                # print("last clicked pos", last_clicked_pos)
                grid.select_hexagon(mouse_pos)
        # if key arrow is pressed, move the camera in the direction of the arrow
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                glTranslatef(-0.1, 0.0, 0.0)
            if event.key == pygame.K_RIGHT:
                glTranslatef(0.1, 0.0, 0.0)
            if event.key == pygame.K_UP:
                glTranslatef(0.0, 0.1, 0.0)
            if event.key == pygame.K_DOWN:
                glTranslatef(0.0, -0.1, 0.0)
            if event.key == pygame.K_w:
                glTranslatef(0.0, 0.0, 0.1)
            if event.key == pygame.K_s:
                glTranslatef(0.0, 0.0, -0.1)
            if event.key == pygame.K_a:
                glRotatef(1, 0, 1, 0)
            if event.key == pygame.K_d:
                glRotatef(-1, 0, 1, 0)
            if event.key == pygame.K_q:
                glRotatef(1, 1, 0, 0)
            if event.key == pygame.K_e:
                glRotatef(-1, 1, 0, 0)
            if event.key == pygame.K_r:
                glRotatef(1, 0, 0, 1)
            if event.key == pygame.K_f:
                glRotatef(-1, 0, 0, 1)
        # print the current val;ues in use by gluLookAt (eye, center, up)
        # print("eye", gluUnProject(0, 0, 0, modelview, projection, viewport))
        # print("center", gluUnProject(screen_width/2, screen_height/2, 0, modelview, projection, viewport))
        # print("up", gluUnProject(0, 1, 0, modelview, projection, viewport))

def main():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.8, 0.8, 0.8, 1.0)
    # grid.draw_grid()
    pygame.display.flip()
    clock = pygame.time.Clock()

    while True:
        handle_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)
        grid.draw_grid()
        pygame.display.flip()
        clock.tick(60)

grid = Grid(rows, cols, world_size, world_h_dist, world_v_dist)
main()