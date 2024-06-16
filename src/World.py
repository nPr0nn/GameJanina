
from .Player import Player
from .BoundingBox import BBox

from . import manageCollisions
from .Camera2D import Camera 

from . import grass
import random 
import math 

class World():
    def __init__(self, grassManager, scale):
        self.entities = [] 
        
        self.player   = Player((1000, 1000))
        self.camera   = Camera(self.player.pos, scale)
 
        self.entities.append(BBox(pos=(0, 300), dim=(5000, 40), color=(255,255,255), grass_interact=False))
        self.entities.append(BBox(pos=(0, 4200), dim=(5000, 40), color=(255,255,255), grass_interact=False))

        self.entities.append(BBox(pos=(600, 0), dim=(40, 5000), color=(255,255,255), grass_interact=False))
        self.entities.append(BBox(pos=(4200, 0), dim=(40, 5000), color=(255,255,255), grass_interact=False))
        
        self.grassManager = grassManager
        self.grassTime    = 0.0
        self.plantGass()

    def plantGass(self):
      for y in range(300):
        y += 5
        for x in range(400):
            x += 5
            v = random.random()
            if v > 0.1:
                self.grassManager.place_tile((x, y), int(v * 12), [0, 1, 2, 3, 4])
        
    def render(self, screen, dt): 
        rot_function = lambda x, y: int(math.sin(self.grassTime / 60 + x / 100) * 15)
        self.grassManager.update_render(screen, dt, offset=self.camera.pos, rot_function=rot_function)
        self.grassTime += dt * 100
        
        for entity in self.entities:
            if entity.grass_interact:
                entity.render(screen, self.camera, dt) 
        self.player.render(screen, self.camera, dt)
            
    def tick(self, dt):
        self.grassManager.apply_force(self.player.pos, 10, 25)

        self.player.pre_tick(dt)
        
        collisions = []       
        for entity in self.entities: 
            hit, col_point, col_normal, col_t, _ = manageCollisions.checkPlayerStaticEntity(self.player, entity) 
            if hit:
                entity.color = (255,0,0)
                collisions.append( (col_t, col_point, col_normal, entity) )
  
        # ordena pela proximidade do player (importante para evitar problemas de colisão simultanea)
        collisions.sort(key=lambda x: x[0])
 
        for collision in collisions:
            col_t, col_point, col_normal, entity = collision
            manageCollisions.resolvePlayerStaticEntity(self.player, entity) 

        self.player.tick(dt)
        self.camera.tick(self.player.pos, dt)

        for entity in self.entities:
            if entity.grass_interact:
                self.grassManager.apply_force(entity.pos + entity.dim/2, entity.dim[0] * 0.8,entity.dim[1] * 0.8) 
            entity.tick(dt)
    
    def input(self, key):
        self.player.input(key)
