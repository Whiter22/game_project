import pygame as pg
import numpy as np

class Bullet(pg.sprite.Sprite):
    def __init__(self, xy, mouse_pos):
        super().__init__()
        self.image = pg.Surface((5,5))
        self.image.fill((255, 255, 255))

        self.start_xy = xy
        self.end_xy = (mouse_pos[0], mouse_pos[1]) 
        self.direction = self.calculate_direction()

        self.rect = self.image.get_rect(topleft = self.start_xy)

    def calculate_direction(self):
        direction = np.array(self.end_xy) - np.array(self.start_xy)
        norm = np.linalg.norm(direction)
        return direction / norm if norm != 0 else (0, 0)

    def move_bullet(self):
        self.rect.topleft = self.start_xy = (self.start_xy[0] + self.direction[0] * 4, self.start_xy[1] + self.direction[1] * 4)

    def update(self):
        self.move_bullet()
