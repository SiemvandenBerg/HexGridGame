#utils.py
import numpy as np
import pygame

screen_width = 800
screen_height = 600

rows = 6
cols = 4
hex_size = 60

dx = 0
dy = 0

initial_screen_pos = (50, 50)


colors = np.full((rows, cols, 3), (255, 255, 255), dtype=int)

screen = pygame.display.set_mode((screen_width, screen_height))
layer1 = pygame.Surface((screen_width, screen_height))
layer1_rect = layer1.get_rect()
layer2 = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
layer2_rect = layer2.get_rect()