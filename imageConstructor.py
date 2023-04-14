import random
import sys
from PIL import Image
import pygame
import ast
from utils import screen

# with open('image.txt', 'r', encoding='utf-8') as f:
#     data = f.read()
#     data = data.strip()
#     imageArrayFromFile = ast.literal_eval(data)

# Function that opens a txt file from terrain_arrays folder based on terrain type and returns imageArrayFromFile

def OpenImageFile(terrain_type):

    with open(f'{terrain_type}.txt', 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.strip()
        imageArrayFromFile = ast.literal_eval(data)
    print("open image file for:" + imageArrayFromFile)
    return imageArrayFromFile

def DrawImageFromSquares(imageArray):
    height, width = len(imageArray), len(imageArray[0])
    surface = pygame.Surface((width, height))
    for y in range(height):
        for x in range(width):
            pygame.draw.rect(surface, imageArray[y][x], (x, y, 1, 1))
    return surface

def MoveImage(image, x, y):
    screen.fill((0, 0, 0))
    screen.blit(image, (x, y))
    pygame.display.update()

def ShuffleRectangles(surface):
    rect_list = []
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            rect_list.append((x, y))
    random.shuffle(rect_list)
    new_surface = pygame.Surface(surface.get_size())  # Create new surface with correct dimensions
    for rect in rect_list:
        color = surface.get_at(rect)
        new_color = surface.get_at(rect_list.pop())
        new_surface.set_at(rect, new_color)
    return new_surface

# pixelArtSurface = DrawImageFromSquares(imageArrayFromFile)
# screen.blit(pixelArtSurface, (0, 0))
# # pygame.display.update()