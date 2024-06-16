
import time
import pygame
from pygame.math import Vector2

from .BoundingBox import BBox

class Player():
    def __init__(self, pos):
        self.pos     = Vector2(pos)
        self.vel     = Vector2([0,0])
       
        self.spritesheet = pygame.image.load("assets/soldier.png").convert_alpha()

        self.speed   = 300
        self.pressed = {'A':0, 'S':0, 'D':0, 'W':0, 'a':0, 's':0, 'd':0, 'w':0}

        box_width  = 20
        box_height = 20
        self.box  = BBox((pos[0] - box_width/2, pos[1] - box_height/2), (box_width, box_height), (123,55,123))
       
    def pre_tick(self, dt):
        self.vel = Vector2([0,0])
        
        if self.pressed['A'] == 1:
            self.vel[0] -= self.speed
        if self.pressed['D'] == 1:
            self.vel[0] += self.speed
        if self.pressed['W'] == 1:
            self.vel[1] -= self.speed
        if self.pressed['S'] == 1:
            self.vel[1] += self.speed

        self.vel = (self.vel).elementwise() * dt
 
    def tick(self, dt):
        self.pos    += self.vel
        self.box.pos = (self.pos[0] - self.box.dim[0]/2, self.pos[1] - self.box.dim[1]/2)

    def render(self, screen, camera):
        radius = 5
        screen_pos = camera.world2screen(self.pos)
        pygame.draw.circle(screen, (255, 0, 0), screen_pos, radius, 0)
        self.box.render(screen, camera)



        pass

    def input(self, tecla: str):
        if tecla.isupper():
            self.pressed[tecla]         = 1
            self.pressed[tecla.lower()] = 0
        if tecla.islower():
            self.pressed[tecla]         = 1
            self.pressed[tecla.upper()] = 0 
