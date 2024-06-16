
import pygame
from pygame.math import Vector2

class Camera():
    def __init__(self, pos, scale):
        self.scale   = scale
        self.pos     = Vector2(pos)
        self.t       = 0

    def tick(self, target):
        window_info = pygame.display.Info()
        offset      = ((window_info.current_w * self.scale)/ 2, (window_info.current_h * self.scale)/ 2)
        self.pos    = target - offset

    def world2screen(self, pos):
        return (pos[0] - self.pos[0], pos[1] - self.pos[1])

    def screen2world(self, pos):
        return (pos[0] + self.pos[0], pos[1] + self.pos[1])
