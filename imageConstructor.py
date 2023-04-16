import random
import sys
from PIL import Image
import pygame
import ast
from utils import screen
import os
import ast

# Function that opens a txt file from terrain_arrays folder based on terrain type and returns imageArrayFromFile

def OpenImageFile(terrain_type):
    cache_dir = 'terrain_cache'

    # clear the cache directory
    # if os.path.exists(cache_dir):
    #     for file in os.listdir(cache_dir):
    #         os.remove(os.path.join(cache_dir, file))
    #         print("cache cleared")

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = os.path.join(cache_dir, f'{terrain_type}.txt')

    # check if the file exists in the cache
    if os.path.exists(cache_file):
        # read the file from the cache
        # print("cached data exists for: " + terrain_type)
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = f.read()
        imageArrayFromFile = ast.literal_eval(data)
    else:
        # create the file and store it in the cache
        # print("cached data does NOT exist for:" + str(terrain_type))
        # print("creating cached data for:" + str(terrain_type))
        # replace spaces with underscores in terrain
        terrain_type = terrain_type.replace(' ', '_')

        if terrain_type + '.txt' in os.listdir('terrain_arrays'):    
            with open(f'terrain_arrays/{terrain_type}.txt', 'r', encoding='utf-8') as f:
                data = f.read()
                data = data.strip()
                imageArrayFromFile = ast.literal_eval(data)
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(str(imageArrayFromFile))
        else:
            # print("no file for:" + terrain_type)
            return None
    return imageArrayFromFile

def DrawImageFromSquares(imageArray):
    height, width = len(imageArray), len(imageArray[0])
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # make the background soft pink

    for y in range(height):
        for x in range(width):
            pygame.draw.rect(surface, imageArray[y][x], (x, y, 1, 1))
    return surface

def MoveImage(image, x, y):
    # screen.fill((0, 0, 0))
    screen.blit(image, (x, y))
    pygame.display.update()

# def ShuffleRectangles(surface):
#     rect_list = []
#     for y in range(surface.get_height()):
#         for x in range(surface.get_width()):
#             rect_list.append((x, y))
#     random.shuffle(rect_list)
#     new_surface = pygame.Surface(surface.get_size())  # Create new surface with correct dimensions
#     for rect in rect_list:
#         color = surface.get_at(rect)
#         new_color = surface.get_at(rect_list.pop())
#         new_surface.set_at(rect, new_color)
#     return new_surface