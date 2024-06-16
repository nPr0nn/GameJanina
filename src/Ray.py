
import pygame
from pygame.math import Vector2

class Ray():
    def __init__(self, origin, direction):
        self.origin = Vector2(origin)
        self.dir    = Vector2(direction)

    def at(self, t):
        return (self.origin + ((self.dir).elementwise()) * t)

    def render(self, screen):
        pygame.draw.line(screen, (255,255,255), self.origin, self.at(100))
