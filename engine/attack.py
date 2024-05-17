
from .entity import Entity


class HurtBox(Entity):
    def __init__(self, parent):
        super().__init__('None', parent.rect.center)
        self.rect.size = (10, 20)
        self.parent = parent
        self.damaged = []
    
    def update(self, dt=None):
        if self.rect.width < 25:
            self.rect.width += 2
        else:
            self.delete()
        
        self.rect.left = self.parent.rect.centerx + 5
        self.rect.centery = self.parent.rect.centery
        
        for e in self.g.entities:
            if e != self.parent and not e in self.damaged and self.rect.colliderect(e.rect):
                self.damaged.append(e)
                e.damage(1)
