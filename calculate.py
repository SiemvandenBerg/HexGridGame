# calulate.py
import numpy as np

# Initialize variables for tracking the game screen position offset
game_screen_offset_x = 0
game_screen_offset_y = 0
dx = 0
dy = 0

def update_game_screen_position(delta_x, delta_y, screenPos):
    new_x = screenPos[0] - delta_x
    new_y = screenPos[1] - delta_y
    return (new_x, new_y)

def point_in_hexagon(x, y, center_x, center_y, size, offset_x=0, offset_y=0):
    # Calculate the vertices of the hexagon
    angle = np.pi/6
    points = []

    center_x += offset_x
    center_y += offset_y

    for i in range(6):
        px = center_x + size * np.cos(angle)
        py = center_y + size * np.sin(angle)
        points.append([px, py])
        angle += np.pi/3
    
    # Use the ray-casting algorithm to determine if the point is inside the hexagon
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(n+1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    
    return inside