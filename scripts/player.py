
import pygame
import engine


class Player(engine.PhysicEntity):
    def __init__(self, pos):
        super().__init__('player', pos)
        self.speed = 20
        self.life = 3
        self.jumps = 1
        self._invincible = 0
        self._dash = 0
        self.attack_obj = None
        self.direction = 0
        self.wall_slide = 0
    
    @property
    def invincible(self):
        return self._invincible > 0
    
    @invincible.setter
    def invincible(self, value):
        if value is False:
            self._invincible = 0
        else:
            self._invincible = value
    
    @property
    def dashing(self):
        return self._dash > 0
    
    def respawn(self, pos):
        self.life = 3
        self.alive = True
        self.rect.topleft = pos
        self.g.entities.add(self)
    
    def jump(self):
        if self.wall_slide:
            if self.last_move[0] > 0:
                self.next_move[0] = -6
                self.vertical_momentum = -5
                self.air_timer = 4
                self.jumps = max(0, self.jumps - 1)
            elif self.last_move[0] < 0:
                self.next_move[0] = 6
                self.vertical_momentum = -5
                self.air_timer = 4
                self.jumps = max(0, self.jumps - 1)
        elif self.jumps:
            self.jumps -= 1
            self.vertical_momentum = -5
            self.air_timer = 4
    
    def dash(self, speed, time, motion):
        self.speed = speed
        self._dash = time
        if motion[0] > 0:
            self.direction = 1
        elif motion[0] < 0:
            self.direction = -1
    
    def attack(self):
        self.attack_obj = engine.HurtBox(self)
        self.g.actions.add(self.attack_obj)
    
    def damage(self, dmg):
        self.life -= dmg
        if self.life <= 0:
            self.alive = False
        else:
            self._invincible = 700
    
    def update(self, dt):
        super().update(dt)
        if self.g.inputs.holding(pygame.K_q):
            self.next_move[0] -= self.speed * dt / 100
        if self.g.inputs.holding(pygame.K_d):
            self.next_move[0] += self.speed * dt / 100
        
        if self.g.inputs.pressed(pygame.K_LSHIFT) and not self.dashing and self.next_move[0]:
            self.dash(150, 17, self.next_move)
        
        if self.dashing:
            self.next_move[0] += self.direction * self.speed * dt / 100
            self._dash -= dt
            if self._dash <= 0:
                self.speed = 20
                self.direction = 0
        
        self.gravity()
        
        self.wall_slide = max(0, self.wall_slide - dt)
        if self.in_air and (self.collisions['right'] or self.collisions['left']):
            self.wall_slide = 1100
        if self.wall_slide:
            self.next_move[1] = min(self.next_move[1], 1)
        
        if self.g.inputs.pressed(pygame.K_SPACE) or self.g.inputs.pressed(pygame.K_z):
            self.jump()
        elif self.g.inputs.holding(pygame.K_LCTRL) or self.g.inputs.holding(pygame.K_s):
            self.dropthrough = True
        elif self.dropthrough:
            self.dropthrough = False
        
        if not self.in_air:
            if self.next_move[0] != 0:
                self.set_action('walk')
            else:
                self.set_action('idle')
            
        self.update_physics()
        
        if self.collisions['bottom']:
            self.jumps = 1
            self.wall_slide = 0
        
        if self.invincible:
            self._invincible -= dt
        
        if self.g.inputs.pressed(pygame.K_f):
            self.attack()
        
    def render(self, surf, scroll):
        super().render(surf, scroll)
        if self.invincible:
            pygame.draw.rect(surf, 'orange', engine.core.offset_rect(self.rect, scroll))
