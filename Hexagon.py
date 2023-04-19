import pygame, numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from terrain_types import terrain_types

class Hexagon:
    def __init__(self, x, y, row, col, radius, thickness, terrain, graphic):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.radius = radius
        self.thickness = thickness
        self.terrain = terrain
        self.graphic = graphic
        self.texture = glGenTextures(1)  # generate a new texture ID
        self.setup_texture()
        self.texture_coords = self.get_texture_coords()

    def setup_texture(self):
        glEnable(GL_TEXTURE_2D) # enable texturing
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix
        texture = glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.graphic.get_width(), self.graphic.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(self.graphic, "RGBA", 1))
        return self.texture

    def get_texture_coords(self):
        coords = []
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x = self.x + self.radius * np.cos(angle)
            y = self.y + self.radius * np.sin(angle)
            s = (x - self.x + self.radius) / (2 * self.radius)
            t = (y - self.y + self.radius) / (2 * self.radius)
            coords.append((s, t))
        return coords

    def draw(self):

        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_LINE_SMOOTH)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

        # Draw the hexagon outline and fill it with color (ie these are the sides of the hexagon)
        glBegin(GL_QUADS)

        # Set the color of the hexagon based on the terrain type 
        terrain_type = terrain_types[self.terrain]
        glColor3f(terrain_type['color'][0], terrain_type['color'][1], terrain_type['color'][2])

        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            x2 = self.x + self.radius * np.cos(angle + np.pi / 3)
            y2 = self.y + self.radius * np.sin(angle + np.pi / 3)
            c = np.clip(0.4 + np.cos(angle) / 2, 0, 1)
            glColor3f(c, c, c)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x2, y2, self.thickness)
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        glBegin(GL_POLYGON) # draw the hexagon
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glTexCoord2f(self.texture_coords[i][0], self.texture_coords[i][1])
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        # Show the texture asociated with the hexagon 
        glEnable(GL_TEXTURE_2D) # enable texturing
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix

        # Draw the hexagon outline
        glLineWidth(3)
         
        glColor3f(0.2, 0.2, 0.2)
        # glColor3f(terrain_type['color'][0], terrain_type['color'][1], terrain_type['color'][2]) # draw the outline in the color of the terrain type

        glBegin(GL_LINE_LOOP)

        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glVertex3f(x1, y1, self.thickness)
        glEnd()
