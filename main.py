import pygame, numpy as np, ast, sys, random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Grid import Grid
from calculate import point_in_hexagon, update_game_screen_position, game_screen_offset_x, game_screen_offset_y, dx, dy
from pathfinding import astar_hex
from drawing import draw_grid
from utils import colors, screen_width, screen_height, rows, cols, hex_size, layer1, layer2, layer1_rect, layer2_rect, screen

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

size = hex_size*0.1
h_dist = size * np.sqrt(3)
v_dist = size * 3/2

verticies = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7), (5,1), (5,4), (5,7))

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Plane(width, height):
    # draw a plane
    glBegin(GL_QUADS)
    glColor3f(1,0,0) # red
    glVertex3f(-width,-height,0) # bottom left red
    glColor3f(0,1,0) # green
    glVertex3f(width,-height,0) # bottom right green
    glColor3f(0,0,1) # blue
    glVertex3f(width,height,0) # top right blue
    glColor3f(1,0,1) # purple
    glVertex3f(-width,height,0) # top left purple
    glEnd()

class Hexagon:
    def __init__(self, x, y, row, col, radius, thickness, color):
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.radius = radius
        self.thickness = thickness
        self.color = color

    def draw(self):
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

        glColor3f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glVertex3f(x1, y1, self.thickness)
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        for i in range(6):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glVertex3f(x1, y1, 0)
        glEnd()

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1, 1, 1, 0.1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(self.x, self.y, self.thickness)
        for i in range(7):
            angle = i * np.pi / 3 + np.pi / 6
            x1 = self.x + self.radius * np.cos(angle)
            y1 = self.y + self.radius * np.sin(angle)
            glVertex3f(x1, y1, self.thickness)
        glEnd()


def get_grid_3d(screenPos, grid):
    global game_screen_offset_x, game_screen_offset_y
    print("draw_grid_3d")
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
            
            # convert 2D coordinates to 3D coordinates
            # center_x_3d, center_y_3d, center_z_3d = grid.convert_to_3d((center_x, center_y))
            
            # create hexagon with 3D coordinates
            # hexagon_3d = Hexagon(center_x, center_y, 1, size, row, col, 'grassland')

            grid.add_hexagon(Hexagon(x=center_x, y=center_y, row=row, col=col, radius=size, thickness=1, color=(1, 1, 0) )) # x and y are 2D coordinates and not 3D coordinates

def print_hexagons(grid):
    if not isinstance(grid, Grid):
        raise TypeError("Expected a Grid object, got " + str(type(grid)))
    for row in grid.hexagons:
        cols = grid.hexagons[row]
        for col in cols:
            hexagon = grid.hexagons[row][col]
            if not isinstance(hexagon, Hexagon):
                raise TypeError("Expected a Hexagon object, got " + str(type(hexagon)))
            # print("row: " + str(row) + " col: " + str(col) + " " + str(hexagon))
            
def draw_hexagons_3d(grid):
    if not isinstance(grid, Grid):
        raise TypeError("Expected a Grid object, got " + str(type(grid)))
    for row in grid.hexagons:
        cols = grid.hexagons[row]
        for col in cols:
            hexagon = grid.hexagons[row][col]
            if not isinstance(hexagon, Hexagon):
                raise TypeError("Expected a Hexagon object, got " + str(type(hexagon)))
            print("row: " + str(row) + " col: " + str(col) + " " + str(hexagon))
            # draw the current hexagon with the 3D coordinates of the hexagon object 
            hexagon.draw()
      
# function that switches between 2d and 3d views of the grid and draws the grid in the correct view mode (unimplemented)
def switch_view_mode():
    global view_mode
    if view_mode == '2d':
        view_mode = '3d'
    else:
        view_mode = '2d'

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
    
    # if viewmode is 2d, draw the grid in 2d
    if view_mode == '2d':
        grid = Grid(rows, cols, terrains, colors)
        grid.init_colors()
        # Draw grid with initial screen position one time to  initialize layer1
        if initial_screen_pos == (0, 0):
            draw_grid(initial_screen_pos, grid)
            initial_screen_pos = (1, 1)    

        pygame.display.flip()
        pygame.time.wait(10)        

        # draw layer 2 on top of layer 1
        screen.blit(layer1, layer1_rect)
        screen.blit(layer2, layer2_rect)

    elif view_mode == '3d':
        grid = Grid(rows, cols, terrains, colors)
        grid.init_colors()
        
        get_grid_3d(screenPos, grid)
        print_hexagons(grid)

        size = 0.1
        h_dist = size * np.sqrt(3)
        v_dist = size * 3/2

        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        gluPerspective(20, (display[0]/display[1]), 0.1, 500.0) # set the perspective of the camera (fov, aspect ratio, near clipping plane, far clipping plane)
        glTranslatef(0.0,0.0, -300) # move the camera back 5 units
        glRotatef(-65, 1, 0, 0) # rotate the camera 65 degrees on the x axis (up and down)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            glDisable(GL_DEPTH_TEST)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            hex_size_3d = hex_size * 0.1
            Plane(50, 50)
            draw_hexagons_3d(grid)

            pygame.display.flip()
            pygame.time.wait(10)        
    else:
        pygame.quit()
pygame.quit()
sys.exit()