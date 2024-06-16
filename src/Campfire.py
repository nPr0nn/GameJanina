import pygame 
from pygame.math import Vector2
from .BoundingBox import BBox

class Campfire():
    def __init__(self, pos, dim, color=(0,0,0)):
        self.pos   = Vector2(pos)
        self.dim   = Vector2(dim)
        self.color = color
        self.vel   = Vector2([0,0])
        self.box = BBox(pos, dim, color)
        self.power = 1

    def tick(self, dt):
        pass

    def render(self, screen, camera, debug):
        screen_pos = camera.world2screen(self.pos)
        
        rect = pygame.Rect(screen_pos[0], screen_pos[1], self.dim[0], self.dim[1])
        # pygame.draw.circle(screen, self.color, self.pos, 5, 0)
        pygame.draw.rect(screen, self.color, rect, width=0) 
        pass
