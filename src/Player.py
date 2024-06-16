
import time
import pygame
from pygame.math import Vector2

import math 
from .utils import Utils
from .BoundingBox import BBox
from .Spritesheet import Spritesheet

class Player():
    def __init__(self, pos):
        self.pos     = Vector2(pos)
        self.vel     = Vector2([0,0])
        self.acc     = Vector2([0,0])
        
        self.flip    = False
       
        self.spritesheet = Spritesheet("assets/soldier.png", 64, 64)
        self.swordsheet  = Spritesheet("assets/sword.png", 128, 128)

        
        self.sword        = self.swordsheet.get_sprite(0, 0)
        self.sword_offset =  Vector2([-26, -20])
        
        self.state        = 'idle'
        self.spriteNumber = 0
        self.stateDict    = {'idle':0, 'moving':1}
 
        self.playerTime   = 0  
        self.swordTime    = 0 
        
        self.ACC     = 300
        self.FRICC   = -0.1
        self.pressed = {'A':0, 'S':0, 'D':0, 'W':0, 'a':0, 's':0, 'd':0, 'w':0}

        box_width  = 20
        box_height = 20
        self.box  = BBox((pos[0] - box_width/2, pos[1] - box_height/2), (box_width, box_height), (123,55,123))

        self.box_sword  = BBox(pos, (box_width, box_height), (123,55,123))
         self.HP = 255
        self.color = (255,255,255)
        self.timeImune = 0
       
    def pre_tick(self, dt):
        self.vel = Vector2([0,0]) 
        self.acc = Vector2([0,0])

        if self.pressed['A'] == 1:
            self.acc[0] = -self.ACC
        if self.pressed['D'] == 1:
            self.acc[0] = self.ACC
        if self.pressed['W'] == 1:
            self.acc[1] = -self.ACC
        if self.pressed['S'] == 1:
            self.acc[1] = self.ACC

        self.acc += self.vel * self.FRICC
        self.vel += self.acc
        self.vel = (self.vel).elementwise() * dt    
        
        if (self.vel[0] != 0 or self.vel[1] != 0):
            self.state = 'moving'
        else:
            self.state = 'idle'

        if self.flip == False and self.vel[0] < 0:
            self.flip = True 
            self.sword_offset = Vector2([-40, -20])
        elif self.flip == True and self.vel[0] > 0:
            self.flip = False
            self.sword_offset = Vector2([-26, -20])
             
    def tick(self, dt):
        self.timeImune-=dt
        self.pos    += self.vel 
        self.box.pos = self.pos - self.box.dim/2
        self.playerTime += dt
        self.swordTime += 1 * dt

    def rotate_surface(self, surface, angle, pivot):
        rotated_surface = pygame.transform.rotate(surface, angle) 
        rotated_rect = rotated_surface.get_rect(center=pivot) 
        return rotated_surface, rotated_rect.topleft
    
    def render(self, screen, camera, debug = False, dt):
        radius = 10
        screen_pos = camera.world2screen(self.pos)
        # self.box.render(screen, camera, dt) 
        # pygame.draw.circle(screen, (255, 0, 0), screen_pos, radius, 0)

        if(self.state == 'idle'):
            self.playerTime = 0 
        elif(self.state == 'moving' and self.playerTime > 1/(5*self.vel.length() + 1e-9) ):
            self.spriteNumber = (self.spriteNumber + 1) % 6
            self.playerTime = 0
 
        sprite        = self.spritesheet.get_sprite(self.spriteNumber, self.stateDict[self.state])
        sprite        = pygame.transform.flip(sprite, self.flip, False)
        sprite_dim    = Vector2(sprite.get_size())
        sprite_center = screen_pos - sprite_dim/2 # center 

        sprite_sword     = pygame.transform.flip(self.sword, False, False)
        sprite_sword_dim = Vector2(sprite_sword.get_size())

        rot_sprite_sword, rot = self.rotate_surface(sprite_sword, 360*math.sin(self.swordTime), sprite_center)
         
        screen.blit(sprite, sprite_center)
        screen.blit(rot_sprite_sword, rot + sprite_sword_dim/2 + self.sword_offset)



    def input(self, tecla: str):
        if tecla.isupper():
            self.pressed[tecla]         = 1
            self.pressed[tecla.lower()] = 0
        if tecla.islower():
            self.pressed[tecla]         = 1
            self.pressed[tecla.upper()] = 0 
