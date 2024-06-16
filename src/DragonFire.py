from pygame.math import Vector2
import pygame

class DragonFire():
    def __init__(self, pos, type, dir, power = 5, color=(255,0,0), world=None):
        # types = shower, fireball, concentrated
        self.life_time = 100
        self.pos   = Vector2(pos)
        self.type  = type
        self.dir   = Vector2(dir)
        self.power = power
        if self.type == "fireball":
            tamanho = power
        elif self.type == "shower":
            tamanho = power/2
            self.life_time = int(self.life_time * 0.1)
        elif self.type == "concentrated":
            tamanho = 1
            self.life_time = 100
            self.life_time = int(self.life_time * 100)
        self.dim = Vector2([tamanho,tamanho])
        self.color = color
        self.world = world

    def tick(self):
        self.pos += self.dir * self.power
        self.life_time -= 1
        

    def render(self, screen, camera):
        screen_pos = camera.world2screen(self.pos)
        pygame.draw.circle(screen, self.color, screen_pos, self.power, 0)
        pass
