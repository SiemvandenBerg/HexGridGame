# Hexagon.py
import pygame, numpy as np
from pygame.locals import *
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from terrain_types import terrain_types
from utils import last_clicked_pos

class Hexagon:
    def __init__(self, row, col, radius, thickness, terrain, graphic, pos):
        self.row = row
        self.col = col
        self.radius = radius[0]
        self.thickness = thickness
        self.terrain = terrain
        self.graphic = graphic
        self.pos = pos
        self.texture = glGenTextures(1)  # generate a new texture ID
        self.texture_coords = self.get_texture_coords()
        self.setup_texture()

    def setup_texture(self):
        glEnable(GL_TEXTURE_2D) # enable texturing
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix
        texture = glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.graphic.get_width(), self.graphic.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(self.graphic, "RGBA", 1))
        return texture

    def get_texture_coords(self):
        coords = []
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x = self.pos[0] + self.radius * np.cos(angle)
            y = self.pos[1] + self.radius * np.sin(angle)
            s = (x - self.pos[0]+ self.radius) / (2 * self.radius)
            t = (y - self.pos[1] + self.radius) / (2 * self.radius)
            coords.append((s, t))
        return coords

    def contains_point(self, point, tolerance=0.01, buffer=0, margin=0):
        n = 6 
        inside = False
        vertices = []
        for i in range(n):
            angle = i * np.pi / 3 + np.pi / 2 # adjust angle calculation
            if i % 2 == 0: # calculate x and y coordinates for top/bottom vertices
                vertices.append((self.pos[0] + (self.radius - buffer ) * np.cos(angle), self.pos[1] + (self.radius - buffer ) * np.sin(angle)))
            else: # calculate x and y coordinates for side vertices
                vertices.append((self.pos[0] + (self.radius - buffer ) * np.cos(angle + np.pi/6), self.pos[1] + (self.radius - buffer ) * np.sin(angle + np.pi/6)))
        j = n - 1
        for i in range(n):
            if ((vertices[i][0] > point[0] - tolerance) != (vertices[j][0] > point[0] - tolerance)) and \
            (point[1] + tolerance < (vertices[j][1] - vertices[i][1]) * (point[0] - vertices[i][0]) / (vertices[j][0] - vertices[i][0]) + vertices[i][1]):
                inside = not inside
            j = i
        return inside

    def draw(self):
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_LINE_SMOOTH)
        # glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

        # draw the hexagon
        glBegin(GL_QUADS)
        terrain_type = terrain_types[self.terrain]
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.pos[0] + self.radius * np.cos(angle)
            y1 = self.pos[1] + self.radius * np.sin(angle)
            x2 = self.pos[0] + self.radius * np.cos(angle + np.pi / 3)
            y2 = self.pos[1] + self.radius * np.sin(angle + np.pi / 3)
            
            c = np.clip(0.4 + np.cos(angle) / 2, 0, 1)
            glColor3f(c, c, c)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x2, y2, self.thickness)
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        # Draw a square base for the hexagon to sit on to avoid z-fighting with the terrain below it
        glBegin(GL_QUADS)
        glColor3f(0.3, 0.3, 0.3)
        glVertex3f(self.pos[0] - self.radius, self.pos[1] - self.radius, 0)
        glVertex3f(self.pos[0] + self.radius, self.pos[1] - self.radius, 0)
        glVertex3f(self.pos[0] + self.radius, self.pos[1] + self.radius, 0)
        glVertex3f(self.pos[0] - self.radius, self.pos[1] + self.radius, 0)
        glEnd()

        # draw the hexagon
        glEnable(GL_TEXTURE_2D) # enable texturing
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # do not show the texture outside the hexagon 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glBegin(GL_POLYGON) # draw the hexagon
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.pos[0] + self.radius * np.cos(angle)
            y1 = self.pos[1] + self.radius * np.sin(angle)
            glTexCoord2f(self.texture_coords[i][0], self.texture_coords[i][1])
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        # stop texturing
        glDisable(GL_TEXTURE_2D)
        
        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix
        # Draw the hexagon's outline
        glLineWidth(3)
        # line color black
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINE_LOOP)
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.pos[0] + self.radius * np.cos(angle)
            y1 = self.pos[1] + self.radius * np.sin(angle)
            glTexCoord2f(self.texture_coords[i][0], self.texture_coords[i][1])
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        glPointSize(5)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(self.pos[0], self.pos[1], 1)
        glEnd() 
        
        glPointSize(15)
        glBegin(GL_POINTS)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(last_clicked_pos[0], last_clicked_pos[1], 0.0)
        glEnd()

        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        # glDisable(GL_DEPTH_TEST)
        glDisable(GL_LINE_SMOOTH)
        glDisable(GL_TEXTURE_2D)

