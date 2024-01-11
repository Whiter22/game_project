import pygame as pg
import random as r
import numpy as np

COLORS = {
    "RED" : (255, 0, 0),
    "GREEN" : (0, 255, 0),
    "BLUE" : (0, 0, 255)
}

USED_XY = set()

class Asteroid(pg.sprite.Sprite):
    # health
    # head_xy (x, y)
    # a = 0
    # b = 0
    ##########################
    # path ax+b (a, b)
    # speed 

    def __init__(self, midd, radius):
        super().__init__()
        global USED_XY
        global COLORS
        self.color = self.get_color()
        self.image = pg.Surface((20, 20))
        self.image.fill(self.color)

        while True:
            self.head_xy = (r.uniform(0.0, 800.0), r.uniform(0.0, 640.0))
            if self.head_xy not in USED_XY and np.linalg.norm(np.array(midd) - np.array(self.head_xy)) >= radius + 300:
                USED_XY.add(self.head_xy)
                break

        self.rect = self.image.get_rect(topleft = self.head_xy)

        if(self.color == COLORS['RED']):
            self.health = 3
        elif(self.color == COLORS['BLUE']):
            self.health = 2
        else:
            self.health = 1

        self._calc_coeff(midd)


    def _calc_coeff(self, midd) -> None:
        points = np.array([midd, self.head_xy])
        x_vals = points[:,0]
        y_vals = points[:,1]

        self.a, self.b = np.polyfit(x_vals, y_vals, deg = 1)


    def get_color(self):
        c = list(COLORS.items())
        rand_color = r.choice(c)
        return rand_color[1]


    def move_y(self, x):
        return self.a*x + self.b
    
    
    def update(self, STEP, midd):
        if self.head_xy[0] < midd[0]:
            new_x = self.head_xy[0] + STEP 
        else: 
            new_x = self.head_xy[0] - STEP
        
        new_y = self.move_y(new_x)
        self.head_xy = (new_x, new_y)
        self.rect.topleft = (new_x, new_y)    