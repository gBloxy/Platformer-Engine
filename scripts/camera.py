
from .core import WIN_SIZE, smooth, clamp


class Camera():
    def __init__(self, game, slowness=0.1):
        self.g = game
        self.scroll = [0, 0]
        self.target = None
        self.slowness = slowness
        self.max_scroll = (game.map.width - WIN_SIZE[0], game.map.height - WIN_SIZE[1])
    
    @property
    def target_pos(self):
        return self.target if type(self.target) in (list, tuple) else self.target.rect.center
    
    def focus(self, target):
        self.target = target
    
    def move(self, movement):
        self.scroll[0] += movement[0]
        self.scroll[1] += movement[1]
    
    def update(self):
        center = self.target_pos
        self.scroll[0] = smooth(self.scroll[0], center[0] - WIN_SIZE[0] // 2, self.g.dt, slowness=self.slowness)
        self.scroll[1] = smooth(self.scroll[1], center[1] - WIN_SIZE[1] // 2, self.g.dt, slowness=self.slowness)
        self.scroll[0] = clamp(self.scroll[0], 0, self.max_scroll[0])
        if self.scroll[1] > self.max_scroll[1]:
            self.scroll[1] = self.max_scroll[1]
