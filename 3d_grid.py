from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

def resize((width, height)):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(width)/height, .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glEnable(GL_DEPTH_TEST)

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    # Draw your sprites here using glBegin and glEnd

pygame.init()
screen = pygame.display.set_mode((800,600), OPENGL|DOUBLEBUF)
resize((800,600))
init()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    render()
    pygame.display.flip()