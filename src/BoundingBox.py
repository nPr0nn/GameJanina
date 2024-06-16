import pygame 
from pygame.math import Vector2

class BBox():
    def __init__(self, pos, dim, color=(0,0,0)):
        self.pos   = Vector2(pos)
        self.dim   = Vector2(dim)
        self.color = color 

    def tick(self, dt):
        pass

    def render(self, screen, camera):
        screen_pos = camera.world2screen(self.pos)
        
        rect = pygame.Rect(screen_pos[0], screen_pos[1], self.dim[0], self.dim[1])
        # pygame.draw.circle(screen, self.color, self.pos, 5, 0)
        pygame.draw.rect(screen, self.color, rect, width=0) 
        pass
