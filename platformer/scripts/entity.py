
import pygame

from .core import data


class Entity():
    def __init__(self, type, pos):
        self.rect = pygame.Rect(pos, data().entities[type]['hitbox'])
        self.img = pygame.Surface(self.rect.size)
    
    def update(self, dt=None):
        pass
        
    def render(self, surf):
        surf.blit(self.img, self.rect)
