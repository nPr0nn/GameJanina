
import pygame
from pygame.math import Vector2

class Spritesheet():
    def __init__(self, path, w, h):
        self.sprite_width  = w
        self.sprite_height = h
        self.sheet = pygame.image.load(path).convert_alpha()

    def get_sprite(self, x, y): 
        sprite = pygame.Surface((self.sprite_width, self.sprite_height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x * self.sprite_width, y * self.sprite_height, self.sprite_width, self.sprite_height))
        return sprite



