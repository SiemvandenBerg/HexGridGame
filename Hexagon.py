import numpy as np

class Hexagon:
    def __init__(self, x, y, z, size, row, col, terrain):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.row = row
        self.col = col
        self.terrain = terrain

    def get_points(self):
        x = self.x
        y = self.y
        z = self.z
        size = self.size
        return [
            (x + size * np.sqrt(3) / 2, y - size / 2, z),
            (x + size * np.sqrt(3), y, z),
            (x + size * np.sqrt(3) / 2, y + size / 2, z),
            (x - size * np.sqrt(3) / 2, y + size / 2, z),
            (x - size * np.sqrt(3), y, z),
            (x - size * np.sqrt(3) / 2, y - size / 2, z),
        ]
