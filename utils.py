# utils.py
import pygame, numpy as np
from pygame.locals import *
from math import sqrt
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
screen_width = 800
screen_height = 600
display = (800, 600)
screen = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
cols = 10
rows = 6
size = 30
h_dist = size
v_dist = size
left = 0
right = 800
bottom = 0
top = 600
near = -1
far = 100
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# glOrtho(left, right, bottom, top, near, far) # gluPerspective(20, (display[0]/display[1]), 0.1, 500.0)
eye_x = 0.0
eye_y = 0.0
eye_z = 1.0
center_x = 0.0
center_y = 0.0
center_z = 0.0
up_x = 0
up_y = 1
up_z = 0

gluPerspective(45.0, float(display[0])/float(display[1]), 0.1, 10.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z) # gluLookAt(x_eye, y_eye, z_eye, x_center, y_center, z_center, x_up, y_up, z_up)
glEnable(GL_LIGHT0)
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.9, 0.9, 0.9, 1.0))
glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 1.0, 1.0, 0.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
projection = glGetDoublev(GL_PROJECTION_MATRIX)
viewport = glGetIntegerv(GL_VIEWPORT)
center_of_world = gluUnProject(screen_width/2, screen_width/2, 0, modelview, projection, viewport) 
world_h_dist = gluUnProject(h_dist, v_dist, 0, modelview, projection, viewport)
world_v_dist = gluUnProject(h_dist, v_dist, 0, modelview, projection, viewport)
world_size = None
world_size = gluUnProject(size, size, 0, modelview, projection, viewport)
last_clicked_pos = gluUnProject(0, 0, 0, modelview, projection, viewport)

glRotatef(-45, 1, 0, 0) # glRotatef(45, 1, 0, 0)
glTranslatef(0.5, 0.0, 0.2)

print("center of world", center_of_world)

initial_screen_pos = (50, 50)
last_clicked_pos = gluUnProject(0, 0, 0, modelview, projection, viewport)


colors = np.full((rows, cols, 3), (255, 255, 255), dtype=int)

screen = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)

layer1 = pygame.Surface((screen_width, screen_height))
layer1_rect = layer1.get_rect()
layer2 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
layer2_rect = layer2.get_rect()