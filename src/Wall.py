

import pygame 
from pygame.math import Vector2
from .BoundingBox import BBox

class Wall():
    def __init__(self, pos, dim, color=(0,0,0), grass_interact=True):
        self.pos   = Vector2(pos)
        self.dim   = Vector2(dim)
        self.color = color 
        self.grass_interact = False
        self.box = BBox(pos, dim, color,grass_interact)
        self.vel = Vector2([0,0])


    def tick(self, dt):
        pass

    def render(self, screen, camera, dt, debug = False):
        pass