import pygame 
from pygame.math import Vector2
import math

from .DragonFire import DragonFire


class Dragon():
        def __init__(self, pos, size, world, color=(255,130,0)):
            self.pos   = Vector2(pos)
            self.size = size
            self.color = color
            self.world = world
            self.player = world.player
            self.vel     = Vector2([0,0])
            self.type_col_box = "circle"
            self.rotation = 0
            self.boca = self.pos + Vector2(self.size, 0)
            self.vel_max = 0.3


        def brain(self):
            # continuo
            if self.player.pos.distance_to(self.pos) > 100:
                self.vel = self.player.pos - self.pos
                self.vel = self.vel.normalize() * self.vel_max
            else:
                self.vel = Vector2(0,0)

            if self.player.pos.distance_to(self.pos) < 150:
                self.world.add_entity(DragonFire(self.boca, "fireball", self.vel, 5, (255,0,0)))
            


        def tick(self):
            self.brain()
            self.pos += self.vel

            # make dragon look for vel direction
            if self.vel.length() > 0:
                dir = self.vel.normalize()
                self.rotation = dir.angle_to(Vector2(1,0))
                self.boca = self.pos + self.size * self.vel.normalize()

             

        def render(self, screen, camera):
            screen_pos = camera.world2screen(self.pos)
            boca_pos = camera.world2screen(self.boca)
            
            pygame.draw.circle(screen, self.color, screen_pos, self.size, 0)
            pygame.draw.circle(screen, (255,0,0), boca_pos, 10, 1)

            pass