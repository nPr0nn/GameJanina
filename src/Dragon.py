import pygame 
from pygame.math import Vector2
import math
import random
from .BoundingBox import BBox
from .DragonFire import DragonFire
from .utils import Utils


class Dragon():
        def __init__(self, pos, size, world, color=(255,127,0)):
            self.pos   = Vector2(pos)
            self.size = size
            self.color = color
            self.world = world
            self.player = world.player
            self.vel     = Vector2([0,0])
            self.type_col_box = "circle"
            self.rotation = 0
            self.boca = self.pos + Vector2(self.size, 0)
            self.vel_max = 30
            self.times()
            self.box = BBox(Vector2(pos[0]-size,pos[1]-size), (size*2, size*2), (255,255,255))
            self.HP = 255


        def times(self):
            self.shower_time_max = 100
            self.concentrated_time_max = 1000
            self.fireball_time_max = 300
            self.concentrated_time = self.concentrated_time_max
            self.shower_time = self.shower_time_max
            self.fireball_time = self.fireball_time_max

        def brain(self):
            # continuo
            if self.player.pos.distance_to(self.pos) > 100:
                self.vel = self.player.pos - self.pos
                self.vel = self.vel.normalize() * self.vel_max
            else:
                self.vel = Vector2(0,0)

            if self.player.pos.distance_to(self.pos) < 200:
                self.shower_time -= 1
                if self.shower_time <= 0:
                    # shot dir eh a direcao do tiro, direcao da velocidade mais um angulo aleatorio
                    shot_dir = self.vel.rotate(random.randint(-50,50))
                    self.world.add_entity(DragonFire(self.boca, "shower", shot_dir, 5, self.world))
            else:
                if self.shower_time < 0:
                    self.shower_time = self.shower_time_max

            if self.player.pos.distance_to(self.pos) < 500:
                self.concentrated_time -= 1
                if self.concentrated_time <= 0:
                    # shot dir eh a direcao do tiro, direcao da velocidade mais um angulo aleatorio
                    shot_dir = self.vel
                    self.world.add_entity(DragonFire(self.boca, "concentrated", shot_dir, 50, self.world))
                    self.concentrated_time = self.concentrated_time_max

            if self.player.pos.distance_to(self.pos) < 350:
                self.fireball_time -= 1
                if self.fireball_time <= 0:
                    # shot dir eh a direcao do tiro, direcao da velocidade mais um angulo aleatorio
                    shot_dir = self.vel.rotate(random.randint(-10,10))
                    self.world.add_entity(DragonFire(self.boca, "fireball", shot_dir, 10, self.world))
                    self.fireball_time = self.fireball_time_max


        def tick(self, dt):
            self.brain()
            self.pos += self.vel*dt
            self.box.pos = Vector2(self.pos[0]-self.size,self.pos[1]-self.size)

            # make dragon look for vel direction
            if self.vel.length() > 0:
                dir = self.vel.normalize()
                self.rotation = dir.angle_to(Vector2(1,0))
                self.boca = self.pos + self.size * self.vel.normalize()

        def hurt(self, damage):
            self.HP = Utils.clamp(self.HP - damage, 0, 255)
            self.color = (127+(self.HP//2), 127, 127-(self.HP//2))

             

        def render(self, screen, camera, debug = False):
            if self.HP > 0:
                screen_pos = camera.world2screen(self.pos)
                boca_pos = camera.world2screen(self.boca)
                
                if debug:
                    pygame.draw.circle(screen, self.color, screen_pos, self.size, 0)
                    pygame.draw.circle(screen, (255,0,0), boca_pos, 10, 1)
                    # self.box.render(screen, camera, debug)
