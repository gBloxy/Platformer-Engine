
import pygame

from .entity import Entity


class Player(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = 20
    
    def update(self):
        motion = [0, 0]
        if self.g.keys[pygame.K_SPACE]:
            self.jump()
        if self.g.keys[pygame.K_q]:
            motion[0] -= self.velocity * self.g.dt / 100
        if self.g.keys[pygame.K_d]:
            motion[0] += self.velocity * self.g.dt / 100
        self.motion = motion
        super().update()
