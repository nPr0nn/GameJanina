
from .Ray import Ray
from .BoundingBox import BBox
from pygame.math import Vector2

def checkRayBox(ray, box):
    inv_dir = Vector2(
        1 / (ray.dir.x) if ray.dir.x != 0 else float('inf'),
        1 / (ray.dir.y) if ray.dir.y != 0 else float('inf')
    )
    t_near  = (box.pos - ray.origin).elementwise() * inv_dir 
    t_far   = (box.pos + box.dim - ray.origin).elementwise() * inv_dir

    if(t_near[0] > t_far[0]):
        t_near[0], t_far[0] = t_far[0], t_near[0]
    if(t_near[1] > t_far[1]):
        t_near[1], t_far[1] = t_far[1], t_near[1]
    if((t_near[0] > t_far[1]) or (t_near[1] > t_far[0])):
        return False, [0,0], [0,0], 0

    t_hit_near = max(t_near[0], t_near[1])
    t_hit_far  = min(t_far[0], t_far[1])

    if(t_hit_far < 0):
        return False, [0,0], [0,0], t_hit_near

    # Collision Happened
    # get point
    col_point = ray.at(t_hit_near)
   
    # get normal
    if(t_near[0] > t_near[1]):
        col_normal     = Vector2(1,0)
        if(inv_dir[0] >= 0):
            col_normal = Vector2(-1,0)
    else:
        col_normal = Vector2(0,1)
        if(inv_dir[1] >= 0):
            col_normal = Vector2(0,-1)
 
    return True, col_point, col_normal, t_hit_near


def checkPlayerStaticEntity(player, static_entity):
    expandedBBox       = BBox((0,0), (0,0))
    expandedBBox.pos   = static_entity.pos - (player.box.dim/2)
    expandedBBox.dim   = static_entity.dim + player.box.dim
    expandedBBox.color = (255,255,0)
   
    ray                                    = Ray(player.pos, player.vel) 
    ray_hit, col_point, col_normal, t_hit_near = checkRayBox(ray, expandedBBox)  
    if ray_hit:
        hit = (t_hit_near >= 0 and t_hit_near < 1)
        return hit, col_point, col_normal, t_hit_near, expandedBBox

    return False, col_point, col_normal, t_hit_near, expandedBBox


def resolvePlayerStaticEntity(player, static_entity):
    hit, col_point, col_normal, t_hit_near, _ = checkPlayerStaticEntity(player, static_entity)   
    if hit:
        reaction_velocity    = Vector2(0, 0)
        reaction_velocity[0] = (1 - t_hit_near) * abs(player.vel[0]) * col_normal[0]
        reaction_velocity[1] = (1 - t_hit_near) * abs(player.vel[1]) * col_normal[1] 
        player.vel           += reaction_velocity
