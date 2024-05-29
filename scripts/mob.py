
from engine import PhysicEntity


class Mob(PhysicEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.life = 3
        self.direction = 1
        self.speed = 15
    
    def damage(self, dmg):
        self.life -= dmg
        if self.life <= 0:
            self.alive = False
    
    def update(self, dt):
        #self.next_move[0] += self.direction * self.speed * dt / 100
        
        self.gravity()
        self.update_physics()
        
        # if self.collisions['left']:
        #     self.direction = 1
        # elif self.collisions['right']:
        #     self.direction = -1
        
        if not self.g.player.invincible and self.rect.colliderect(self.g.player.rect):
            self.g.player.damage(1)
