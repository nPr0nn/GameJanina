from pygame.math import Vector2
from .BoundingBox import BBox
import pygame

class Particle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.maxlife = randint(13 + int(sliders[0]*5), 27 + int(sliders[0]*10))
        self.life = self.maxlife
        self.dir = choice((-2, -1, 1, 2))
        self.sin = randint(-10, 10)/7
        self.sinr = randint(5, 10)
        self.r = randint(0,2)

        self.ox = randint(-1, 1)
        self.oy = randint(-1, 1)

 
class DragonFire():
    def __init__(self, pos, type, dir, power = 5, world=None):
        # types = shower, fireball, concentrated
        self.life_time = 1000
        self.pos   = Vector2(pos)
        self.type  = type
        self.vel   = Vector2(dir)
        self.power = power
        if self.type == "fireball":
            self.color = (255,0,0)
            self.tamanho = 5
        elif self.type == "shower":
            self.color = (255,120,0)
            self.tamanho = 4*1.5
            self.life_time = int(self.life_time * 0.3)
        elif self.type == "concentrated":
            self.color = (150,150,255)
            self.tamanho = 5
        self.dim = Vector2([self.tamanho,self.tamanho])

        self.box = BBox(pos, self.dim, self.color)

        self.world = world
        self.time = 0

    def tick(self, dt):
        self.pos += self.vel * 10 * dt
        self.life_time -= 1
        if self.life_time <= 0:
            self.world.remove_entity(self)
        self.box.pos = self.pos


    def render(self, screen, camera, dt, debug = False):
        if debug:
            screen_pos = camera.world2screen((self.pos).elementwise()+self.tamanho//2)
            pygame.draw.circle(screen, self.color, screen_pos, self.tamanho, 0)
