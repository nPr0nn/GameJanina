import pygame 
from pygame.math import Vector2

class BBox():
    def __init__(self, pos, dim, color=(0,0,0), grass_interact=True):
        self.pos   = Vector2(pos)
        self.dim   = Vector2(dim)
        self.color = color 

        self.grass_interact = False

    def tick(self, dt):
        pass

    def render(self, screen, camera, dt):
        screen_pos = camera.world2screen(self.pos)
        
        rect = pygame.FRect(screen_pos[0], screen_pos[1], self.dim[0], self.dim[1])
        # pygame.draw.circle(screen, self.color, self.pos, 5, 0)
        pygame.draw.rect(screen, self.color, rect, width=0) 
        pass
