# drawing.py
import numpy as np
import pygame
import pygame.mask
from utils import rows, cols, hex_size, layer2
from calculate import game_screen_offset_x, game_screen_offset_y
from imageConstructor import DrawImageFromSquares, OpenImageFile
from terrain_types import terrain_types
pygame.font.init()
font = pygame.font.SysFont("Arial", 16)
screenPos = (0, 0)



