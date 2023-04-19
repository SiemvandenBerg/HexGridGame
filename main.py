import pygame, numpy as np, ast, sys, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Grid import Grid
from calculate import point_in_hexagon, update_game_screen_position, game_screen_offset_x, game_screen_offset_y, dx, dy
from pathfinding import astar_hex
# from drawing import draw_hexagon
from utils import colors, screen_width, screen_height, rows, cols, hex_size, layer1, layer2, layer1_rect, layer2_rect
from terrain_types import terrain_types

pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
terrains = np.random.choice(['grassland', 'swamp', 'forest', 'dark forest', 'hills', 'mountains', 'water'], (rows, cols), p=[0.45, 0.02, 0.45, 0.02, 0.02, 0.02, 0.02])
start = None
end = None
screenPos = (0, 0)
initial_screen_pos = (0, 0) 

running=True
selected_hexagon = None
right_mouse_down = False
prev_mouse_pos = None

layer1.fill((200, 200, 200))  # Fill layer 1 with grey color

display = (800, 600)
view_mode = '3d'

size = 0.5
h_dist = size * np.sqrt(3)
v_dist = size * 3/2

verticies = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

class Hexagon:
    def __init__(self, x, y, row, col, radius, thickness, color):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.radius = radius
        self.thickness = thickness
        self.color = color
        
        # Initialize the texture object
        # print("Current OpenGL state:", glGetIntegerv(GL_CURRENT_PROGRAM))
        self.texture = glGenTextures(1)
        self.setup_texture()
        self.texture_coords = self.get_texture_coords()

    def setup_texture(self):
        graphic = get_terrain_graphic('grassland') # x, y, radius, thickness, color
        glEnable(GL_TEXTURE_2D) # enable texturing
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, graphic.get_width(), graphic.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(graphic, "RGBA", 1)) 
        # texture, level of detail, internal format, width, height, border, format, type, pixels

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
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

        # Draw the hexagon outline and fill it with color (ie these are the sides of the hexagon)
        glBegin(GL_QUADS)
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

        glMatrixMode(GL_MODELVIEW) # switch back to modelview matrix

        glLineWidth(4)
        glBegin(GL_LINE_LOOP)
        glColor3f(0, 0, 0)
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glVertex3f(x1, y1, self.thickness + 0.01)
        glEnd()

        def cleanup(self):
        # Delete the texture object
            glDeleteTextures(self.texture)

def get_terrain_images(terrain_types):
    terrain_images = {}
    for terrain in terrain_types:
        terrain = terrain.replace(' ', '_')
        image = pygame.image.load('terrain_images/' + terrain + '.jpg')
        terrain_images[terrain] = image
    return terrain_images
terrain_images = get_terrain_images(terrain_types)

def draw_hexagon_2d(center_x, center_y, size, row, col, layer, grid):
    terrain_type = grid.get_terrain(row, col)
    get_terrain_graphic(center_x, center_y, size, row, col, terrain_type, layer)
    draw_hexagon_border(center_x, center_y, size, row, col, layer)

def draw_hexagon_border(center_x, center_y, size, row, col, layer):
    points = get_points(center_x, center_y, size)
    border_color = (0, 85, 128) 
    border_width = 3 
    for i in range(len(points)-1):
        pygame.draw.line(layer, border_color, points[i], points[i+1], border_width)
    text = font.render(f"({row}, {col})", True, (255, 255, 255))
    text_rect = text.get_rect(center=(center_x, center_y))
    layer.blit(text, text_rect)

def get_terrain_graphic(terrain_type):
    terrain_image = terrain_images[terrain_type]
    return terrain_image

test_terrain_graphic = get_terrain_graphic(terrain_type='forest')

def get_hexagon_shape(center_x, center_y, size):
    surface = pygame.Surface(size=(hex_size, hex_size), flags=pygame.SRCALPHA)    
    points = get_points(center_x, center_y, size)
    pygame.draw.polygon(surface=surface, color=(255, 255, 255, 255), points=points)
    return surface 

def get_points(center_x, center_y, size):
    points = []
    angle = np.pi/6  
    for i in range(6):
        x = center_x + size * np.cos(angle)
        y = center_y + size * np.sin(angle)
        points.append([x,y])
        angle += np.pi/3
    points.append(points[0])
    return points

def get_grid(screenPos, grid):
    global game_screen_offset_x, game_screen_offset_y
    game_screen_offset_x = screenPos[0] 
    game_screen_offset_y = screenPos[1]
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
            grid.add_hexagon(Hexagon(x=center_x, y=center_y, row=row, col=col, radius=size, thickness=0.1, color=(0.3, 0.3, 0.7) ))

def draw_hexagons(grid):
    for row in grid.hexagons:
        cols = grid.hexagons[row]
        for col in cols:
            hexagon = grid.hexagons[row][col]
            if view_mode == '3d':
                hexagon.draw()
            elif view_mode == '2d':
                draw_hexagon_2d(center_x=hexagon.x, center_y=hexagon.y, size=hexagon.radius, row=hexagon.row, col=hexagon.col, layer=layer2, grid=grid)
      
grid = Grid(rows, cols, terrains, colors)
grid.init_colors()

while running:
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
                                    get_grid(screenPos, grid)
                                    pygame.display.update()
                                    start = None
                                    end = None

        # Draw grid with initial screen position one time to  initialize layer1
        if initial_screen_pos == (0, 0):
            draw_hexagons(grid)
            initial_screen_pos = (1, 1)    

        pygame.display.flip()
        pygame.time.wait(10)        

        # draw layer 2 on top of layer 1
        # screen.blit(layer1, layer1_rect)
        # screen.blit(layer2, layer2_rect)

    elif view_mode == '3d':

        h_dist = size * np.sqrt(3)
        v_dist = size * 3/2

        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        # initialize OpenGL
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(20, (display[0]/display[1]), 0.1, 500.0) # set the perspective of the camera (fov, aspect ratio, near clipping plane, far clipping plane)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_TEXTURE_2D) # This line enables texturing

        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 1.0, 1.0, 0.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

        glTranslatef(.5, .5, -15) # move the camera back 150 units and right -50 units
        glRotatef(-45, 1, 0, 0) # rotate the camera 65 degrees on the x axis (up and down)

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
            get_grid(initial_screen_pos, grid)
            draw_hexagons(grid)
        
            # rotate the camera 1 degree on the z axis
            # glRotatef(1, 0, 0, 1)

            pygame.display.flip()
            pygame.time.wait(10)        
    else:
        pygame.quit()
pygame.quit()
sys.exit()