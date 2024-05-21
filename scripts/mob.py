
from engine import PhysicEntity


class Mob(PhysicEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.life = 3
    
    def damage(self, dmg):
        self.life -= dmg
        if self.life <= 0:
            self.alive = False
    
    def update(self, dt=None):
        self.gravity()
        self.update_physics()
        if not self.g.player.invincible and self.rect.colliderect(self.g.player.rect):
            self.g.player.damage(1)
