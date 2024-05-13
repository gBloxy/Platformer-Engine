
import pygame

from .core import TILE_SIZE, offset_rect
import scripts.core as core


class Entity():
    def __init__(self, type, pos):
        self.type = type
        self.g = core.game
        self.alive = True
        self.physics = None
        
        # self.rect = pygame.Rect(pos, core.game.data.entities[type]['hitbox'])
        # self.img = pygame.Surface(self.rect.size)
        
        self.img = self.g.asset['GraveRobber']
        self.rect = self.img.get_rect(topleft=pos)
    
    @property
    def map_pos(self):
        return (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
    
    @property
    def in_air(self):
        return self.air_timer > 6
    
    @property
    def in_map(self):
        pos = self.map_pos
        return 0 <= pos[0] <= self.g.map.cols - 1 and 0 <= pos[1] <= self.g.map.rows - 1
    
    def update(self, dt=None):
        pass
    
    def render(self, surf, scroll):
        rect = offset_rect(self.rect, scroll)
        surf.blit(self.img, rect)
        pygame.draw.rect(surf, 'red', rect, 1)


class PhysicEntity(Entity):
    def __init__(self, type, pos):
        super().__init__(type, pos)
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        self.motion = [0, 0]
        self.vertical_momentum = 0
        self.air_timer = 0
        self.dropthrough = False
        self.physics = 'entity'
        self.velocity = 1
    
    def process_physics(self, motion, collideables):
        for tile in collideables:
            if self.rect.colliderect(tile.rect):
                
                if tile.physics == 'solid':
                    if motion[0] > 0:
                        self.rect.right = tile.rect.left
                        self.collisions['right'] = True
                    elif motion[0] < 0:
                        self.rect.left = tile.rect.right
                        self.collisions['left'] = True
            
                    if motion[1] > 0:
                        self.rect.bottom = tile.rect.top
                        self.collisions['bottom'] = True
                    elif motion[1] < 0:
                        self.rect.top = tile.rect.bottom
                        self.collisions['top'] = True
                
                elif tile.physics == 'rampr':
                    if (motion[1] > 0) or (motion[0] > 0):
                        check_x = (self.rect.right - tile.rect.left) / tile.rect.width
                        if 0 <= check_x <= 1:
                            if self.rect.bottom > (1 - check_x) * tile.rect.height + tile.rect.top:
                                self.rect.bottom = (1 - check_x) * tile.rect.height + tile.rect.top
                                self.collisions['bottom'] = True
                
                elif tile.physics == 'rampl':
                    if (motion[1] > 0) or (motion[0] < 0):
                        check_x = (self.rect.left - tile.rect.left) / tile.rect.width
                        if 0 <= check_x <= 1:
                            if self.rect.bottom > check_x * tile.rect.height + tile.rect.top:
                                self.rect.bottom = check_x * tile.rect.height + tile.rect.top
                                self.collisions['bottom'] = True
                
                elif tile.physics == 'dropthrough':
                    if not self.dropthrough:
                        if (motion[1] > 0):
                            if (self.rect.bottom > tile.rect.top) and (self.rect.bottom - motion[1] <= tile.rect.top + 1):
                                self.rect.bottom = tile.rect.top
                                self.collisions['bottom'] = True
    
    def move(self, motion):
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        self.rect.x += motion[0]
        collideables = self.g.map.get_neighbors(self.map_pos) if self.in_map else []
        self.process_physics((motion[0], 0), collideables)
        self.rect.y += motion[1]
        collideables = self.g.map.get_neighbors(self.map_pos) if self.in_map else []
        self.process_physics((0, motion[1]), collideables)
        
    def update_physics(self):
        self.motion[1] += self.vertical_momentum
        
        self.vertical_momentum += 0.3
        if self.vertical_momentum > 7:
            self.vertical_momentum = 7
        
        self.move(self.motion)
        
        if self.collisions['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        elif self.collisions['top']:
            self.vertical_momentum = 0
            self.air_timer += 1
        else:
            self.air_timer += 1
    
    def jump(self):
        if self.air_timer < 6:
            self.vertical_momentum = -5
    
    def update(self, dt=None):
        self.update_physics()
        
        for tile in self.g.map.get_neighbors(self.map_pos) if self.in_map else []:
            pygame.draw.rect(self.g.display, 'blue', offset_rect(tile.rect, self.g.cam.scroll), 1)


class EntityGroup():
    def __init__(self):
        self.entities = []
    
    def add(self, entity):
        self.entities.append(entity)
    
    def remove(self, entity):
        self.entities.remove(entity)
    
    def update(self, dt):
        for e in self.entities:
            e.update(dt)
            if not e.alive:
                self.remove(e)
    
    def render(self, surf, scroll):
        for e in self.entities:
            e.render(surf, scroll)
