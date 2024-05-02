
from .core import WIN_SIZE


class Camera():
    def __init__(self):
        self.scroll = [0, 0]
        self.zoom = 1
        self.target = None
    
    def focus(self, target):
        self.target = target
    
    def update(self):
        center = self.target if type(self.target) in (list, tuple) else self.target.rect.center
        self.scroll = (int(center[0] - WIN_SIZE[0] // 2), int(center[1] - WIN_SIZE[1] // 2))
