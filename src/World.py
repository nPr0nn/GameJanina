
from .Player import Player
from .BoundingBox import BBox
from .Dragon import Dragon

from . import manageCollisions
from .Camera2D import Camera 

from . import grass
import random 
import math 

class World():
    def __init__(self, grassManager, scale):
        self.entities = [] 
        self.player   = Player((0, 0))
        self.camera   = Camera(self.player.pos, scale)
 
        self.entities.append(BBox(pos=(300, 300), dim=(40, 40), color=(255,255,255)))
        self.entities.append(BBox(pos=(500, 500), dim=(40, 40), color=(255,255,255)))
        self.entities.append(BBox(pos=(500, 700), dim=(60, 100), color=(255,255,255)))

        self.dragon = Dragon(pos=(200, 0), size=100, world = self)

        self.grassManager = grassManager
        self.grassTime    = 0.0
        self.plantGass()

    def plantGass(self):
      for y in range(50):
        y += 5
        for x in range(50):
            x += 5
            v = random.random()
            if v > 0.1:
                self.grassManager.place_tile((x, y), int(v * 12), [0, 1, 2, 3, 4])
        
    def render(self, screen, dt): 
        rot_function = lambda x, y: int(math.sin(self.grassTime / 60 + x / 100) * 15)
        
        self.grassManager.update_render(screen, dt, offset=self.camera.pos, rot_function=rot_function)
        self.grassTime += dt * 100

        self.player.render(screen, self.camera)
        for entity in self.entities:
            entity.render(screen, self.camera) 
        self.dragon.render(screen, self.camera)
            
    def tick(self):
        self.grassManager.apply_force(self.player.pos, 10, 25)

        self.player.pre_tick()
        
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

        self.player.tick()
        self.dragon.tick()
        self.camera.tick(self.player.pos)

        for entity in self.entities:
            entity.tick()

    def add_entity(self, entity):
        self.entities.append(entity)
    
    def input(self, key):
        self.player.input(key)
