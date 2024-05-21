
import pygame

from .element import Element
from .core import TILE_SIZE, offset_rect


class Entity(Element):
    def __init__(self, type, pos):
        super().__init__()
        self.type = type
        self.alive = True
        self.physics = None
        self.action = ''
        self.flip = False
        self.animation = None
        
        if type == 'None':
            self.rect = pygame.Rect(pos, (18, 24))
            self.default_img = pygame.Surface(self.rect.size)
            self.config = {}
        else:
            self.config = self.g.data.sprites[type]
            self.default_img = self.config.image
            self.rect = pygame.Rect(pos, self.config['hitbox'])
    
    @property
    def img(self):
        return pygame.transform.flip(self.animation.img, self.flip, False) if self.animation else self.default_img
    
    @property
    def map_pos(self):
        return (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
    
    @property
    def in_map(self):
        pos = self.map_pos
        return 0 <= pos[0] <= self.g.map.cols - 1 and 0 <= pos[1] <= self.g.map.rows - 1
    
    def delete(self):
        self.alive = False
    
    def set_action(self, action):
        if self.action != action:
            self.action = action
            self.animation = self.config.get_anim(action)
    
    def update(self, dt):
        if self.animation:
            self.animation.update(dt)
    
    def render(self, surf, scroll):
        rect = offset_rect(self.rect, scroll)
        surf.blit(self.img, rect)
        # pygame.draw.rect(surf, 'red', rect, 1)


class PhysicEntity(Entity):
    def __init__(self, type, pos):
        super().__init__(type, pos)
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        self.vertical_momentum = 0
        self.air_timer = 0
        self.dropthrough = False
        self.physics = 'entity'
        self.speed = 1
        self.last_move = (0, 0)
        self.next_move = [0, 0]
    
    @property
    def in_air(self):
        return self.air_timer > 3
    
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
    
    def process_moving(self, movement):
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        self.rect.x += movement[0]
        collideables = self.g.map.get_neighbors(self.map_pos) if self.in_map else []
        self.process_physics((movement[0], 0), collideables)
        self.rect.y += movement[1]
        collideables = self.g.map.get_neighbors(self.map_pos) if self.in_map else []
        self.process_physics((0, movement[1]), collideables)
    
    def move(self, motion):
        self.next_move[0] += motion[0]
        self.next_move[1] += motion[1]
    
    def gravity(self):
        self.next_move[1] += self.vertical_momentum
        self.vertical_momentum += 0.3
        if self.vertical_momentum > 7:
            self.vertical_momentum = 7
    
    def update_physics(self):
        self.process_moving(self.next_move)
        
        if self.collisions['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        elif self.collisions['top']:
            self.vertical_momentum = 0
            self.air_timer += 1
        else:
            self.air_timer += 1
        
        self.last_move = tuple(self.next_move)
        self.next_move = [0, 0]
        
        if self.last_move[0] > 0:
            self.flip = False
        elif self.last_move[0] < 0:
            self.flip = True


class EntityGroup():
    def __init__(self):
        self.entities = []
    
    def __getitem__(self, key):
        return self.entities[key]
    
    def __iter__(self):
        return self.entities.__iter__()
    
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
