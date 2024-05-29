
from math import sin, cos, radians
import pygame
import engine

class Bullet(engine.Entity):
    def __init__(self, parent, angle=None):
        super().__init__('bullet', parent.rect.center)
        self.parent = parent
        self.rect.center = parent.rect.center
        if angle is None:
            if parent.flip:
                angle = 180
            else:
                angle = 0
        self.speed = 30
        self.angle = radians(angle)
        self.cos = cos(self.angle)
        self.sin = sin(self.angle)
        self.default_img = pygame.transform.rotate(self.default_img, 360-angle)
    
    def update(self, dt):
        self.rect.x += self.cos * self.speed * dt / 100
        self.rect.y += self.sin * self.speed * dt / 100
        
        for e in self.g.entities:
            if e != self.parent:
                if self.rect.colliderect(e.rect):
                    e.damage(1)
                    self.alive = False
                    break
        
        if not self.in_map:
            self.alive = False
        else:
            collideables = self.g.map.get_neighbors(self.map_pos)
            for tile in collideables:
                if self.rect.colliderect(tile.rect):
                    self.alive = False
                    break
