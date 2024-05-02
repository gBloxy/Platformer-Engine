
import pygame

from .core import data, TILE_SIZE
import scripts.core as core


class Entity():
    def __init__(self, type, pos):
        self.type = type
        self.g = core.game
        self.rect = pygame.Rect(pos, data().entities[type]['hitbox'])
        self.img = pygame.Surface(self.rect.size)
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        self.motion = [0, 0]
        self.velocity = 0
        self.vertical_momentum = 0
        self.air_timer = 0
    
    @property
    def map_pos(self):
        return (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
    
    @property
    def in_air(self):
        return self.air_timer > 6
    
    def process_physics(self, motion, collideables):
        self.collisions = {i:False for i in {'left', 'right', 'top', 'bottom'}}
        old = self.rect.topleft
        
        self.rect.x += motion[0]
        for tile in collideables:
            rect = tile.rect
            if self.rect.colliderect(rect):
                if motion[0] > 0:
                    self.rect.right = rect.left
                    self.collisions['right'] = True
                elif motion[0] < 0:
                    self.rect.left = rect.right
                    self.collisions['left'] = True
        
        self.rect.y += motion[1]
        for tile in collideables:
            rect = tile.rect
            if self.rect.colliderect(rect):
                if motion[1] > 0:
                    self.rect.bottom = rect.top
                    self.collisions['bottom'] = True
                elif motion[1] < 0:
                    self.rect.top = rect.bottom
                    self.collisions['top'] = True
        
        self.motion = [self.rect.x - old[0], self.rect.y - old[1]]
    
    def update_physics(self):
        self.motion[1] += self.vertical_momentum
        
        self.vertical_momentum += 0.3
        if self.vertical_momentum > 4.5:
            self.vertical_momentum = 4.5
        
        self.process_physics(self.motion, self.g.map.get_neighbors(self.map_pos))
        
        if self.collisions['bottom']:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1
    
    def jump(self):
        if self.air_timer < 6:
            self.vertical_momentum = -5
    
    def update(self, dt=None):
        self.update_physics()
        
        for tile in self.g.map.get_neighbors(self.map_pos):
            pygame.draw.rect(self.g.display, 'blue', (tile.rect.x - self.g.cam.scroll[0], tile.rect.y - self.g.cam.scroll[1], *tile.rect.size), 1)
        
    def render(self, surf):
        rect = (self.rect.x - self.g.cam.scroll[0], self.rect.y - self.g.cam.scroll[1], *self.rect.size)
        surf.blit(self.img, rect)
        pygame.draw.rect(surf, 'red', rect, 1)
