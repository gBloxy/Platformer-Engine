
import pygame

from .entity import PhysicEntity


class Player(PhysicEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = 20
    
    def update(self, dt=None):
        motion = [0, 0]
        if self.g.inputs.holding(pygame.K_q):
            motion[0] -= self.velocity * self.g.dt / 100
        if self.g.inputs.holding(pygame.K_d):
            motion[0] += self.velocity * self.g.dt / 100
        if self.g.inputs.pressed(pygame.K_SPACE):
            self.jump()
        elif self.g.inputs.holding(pygame.K_LCTRL):
            self.dropthrough = True
        elif self.dropthrough:
            self.dropthrough = False
        self.motion = motion
        super().update()
