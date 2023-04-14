#utils.py
import numpy as np
import pygame

screen_width = 800
screen_height = 600

rows = 20
cols = 20
hex_size = 40

dx = 0
dy = 0

initial_screen_pos = (50, 50)


colors = np.full((rows, cols, 3), (255, 255, 255), dtype=int)

screen = pygame.display.set_mode((screen_width, screen_height))