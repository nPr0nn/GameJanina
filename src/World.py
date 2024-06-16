import pygame

from .Player import Player
from .BoundingBox import BBox
from .Dragon import Dragon
from .DragonFire import DragonFire
from .Campfire import Campfire

from . import manageCollisions
from .Camera2D import Camera 

from .Dragon import Dragon

from . import grass
import random 
import math 

class World():
    def __init__(self, grassManager, scale):
        self.entities = [] 
        self.player   = Player((0, 0))
        self.camera   = Camera(self.player.pos, scale)
 
        self.entities.append(Campfire(pos=(300, 300), dim=(40, 40), color=(255,255,255)))
        self.entities.append(Campfire(pos=(500, 500), dim=(40, 40), color=(255,255,255)))
        self.entities.append(Campfire(pos=(500, 700), dim=(60, 100), color=(255,255,255)))

        self.dragon = Dragon(pos=(200, 0), size=100, world = self)

        self.grassManager = grassManager
        self.grassTime    = 0.0
        self.plantGass()


        # musica available on https://www.youtube.com/watch?v=s19CtWzNVP4
        pygame.mixer.music.load("assets/junina8bits.mp3")
        pygame.mixer.music.play(-1)

    def plantGass(self):
      for y in range(50):
        y += 5
        for x in range(50):
            x += 5
            v = random.random()
            if v > 0.1:
                self.grassManager.place_tile((x, y), int(v * 12), [0, 1, 2, 3, 4])
        
    def render(self, screen, dt, debug = False): 
        rot_function = lambda x, y: int(math.sin(self.grassTime / 60 + x / 100) * 15)
        
        self.grassManager.update_render(screen, dt, offset=self.camera.pos, rot_function=rot_function)
        self.grassTime += dt * 100

        self.player.render(screen, self.camera, debug = debug)
        for entity in self.entities:
            entity.render(screen, self.camera, debug = debug) 
        self.dragon.render(screen, self.camera, debug = debug)
            
    def tick(self, dt):
        self.grassManager.apply_force(self.player.pos, 10, 25)

        self.player.pre_tick(dt)
        
        collisions = []       
        for entity in self.entities: 
            hit, col_point, col_normal, col_t, _ = manageCollisions.checkPlayerStaticEntity(self.player, entity) 
            if hit:
                if isinstance(entity, DragonFire):
                    self.player.hurt(entity.power)
                    self.entities.remove(entity)
                else:
                    if isinstance(entity, Campfire):
                        entity.power = 1
                    collisions.append( (col_t, col_point, col_normal, entity) )


            else:
                hit, col_point, col_normal, col_t, _ = manageCollisions.checkPlayerStaticEntity(entity, self.player) 
                if hit:
                    if isinstance(entity, DragonFire):
                        self.player.hurt(entity.power)
                        self.entities.remove(entity)
                    else:
                        collisions.append( (col_t, col_point, col_normal, entity) )
  

            if isinstance(entity, Campfire):
                rec1 = pygame.Rect(entity.box.pos, entity.box.dim)
                rec2 = pygame.Rect(self.dragon.box.pos, self.dragon.box.dim)
                if pygame.Rect.colliderect(rec1, rec2):
                    self.dragon.hurt(entity.power)

  
        # ordena pela proximidade do player (importante para evitar problemas de colisão simultanea)
        collisions.sort(key=lambda x: x[0])
 
        for collision in collisions:
            col_t, col_point, col_normal, entity = collision
            manageCollisions.resolvePlayerStaticEntity(self.player, entity) 


        self.player.tick(dt)
        self.dragon.tick(dt)
        self.camera.tick(self.player.pos, dt)


        for entity in self.entities:
            self.grassManager.apply_force(entity.pos + entity.dim/2, entity.dim[0] * 0.8,entity.dim[1] * 0.8) 
            entity.tick(dt)

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def input(self, key):
        self.player.input(key)
