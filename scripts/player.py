
import pygame

import engine


class Player(engine.PhysicEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = 20
        self.life = 3
        self._invincible = 0
        self.attack_obj = None
    
    @property
    def invincible(self):
        return self._invincible > 0
    
    @invincible.setter
    def invincible(self, value):
        if value is False:
            self._invincible = 0
        else:
            self._invincible = value
    
    def damage(self, dmg):
        self.life -= dmg
        if self.life <= 0:
            self.alive = False
        else:
            self._invincible = 700
    
    def attack(self):
        self.attack_obj = engine.HurtBox(self)
        self.g.actions.add(self.attack_obj)
    
    def update(self, dt):
        if self.invincible:
            self._invincible -= dt
        
        motion = [0, 0]
        if self.g.inputs.holding(pygame.K_q):
            motion[0] -= self.velocity * self.g.dt / 100
        if self.g.inputs.holding(pygame.K_d):
            motion[0] += self.velocity * self.g.dt / 100
        if self.g.inputs.pressed(pygame.K_SPACE) or self.g.inputs.pressed(pygame.K_z):
            self.jump()
        elif self.g.inputs.holding(pygame.K_LCTRL) or self.g.inputs.holding(pygame.K_s):
            self.dropthrough = True
        elif self.dropthrough:
            self.dropthrough = False
        self.motion = motion
        
        super().update()
        
        if self.g.inputs.pressed(pygame.K_f):
            self.attack()
    
    def render(self, surf, scroll):
        super().render(surf, scroll)
        if self.invincible:
            pygame.draw.rect(surf, 'orange', engine.core.offset_rect(self.rect, scroll))
