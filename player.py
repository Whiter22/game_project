import pygame as pg
from bullet import Bullet

class Player(pg.sprite.Sprite):
    def __init__(self, midd):
        super().__init__()
        self.health = 3
        self.radius = 60
        self.image = pg.Surface((120, 120), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        pg.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), 20)
        self.rect = self.image.get_rect(center=midd)

        self.bullets = pg.sprite.Group()

    # def get_input(self, end, mouse_pos):
    #     mouse_b = pg.mouse.get_pressed()

    #     if mouse_b[0]:
    #         self.bullets.add(Bullet(end, tuple(mouse_pos)))

    def update(self, surface):
        # self.get_input(end, mouse_pos)
        self.bullets.update()
        self.bullets.draw(surface)
    