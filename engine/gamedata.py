
from os.path import join
import pygame

from .element import Element
from .core import read_json
from .animation import Animation, load_imgs


class SpriteData(Element):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.animations = {}
        
        if 'colorkey' in config:
            self.colorkey = config['colorkey']
        else:
            self.colorkey = None
        
        if 'image' in config:
            self.image = pygame.image.load(join(self.g.asset.path, 'textures', config['image']))
            if self.colorkey:
                self.image.set_colorkey(self.colorkey)
        
        if 'animations' in config:
            for name in config['animations']:
                anim = config['animations'][name]
                path = join(self.g.asset.path, 'textures', anim['path'])
                imgs = load_imgs(path, self.colorkey)
                loop = anim['loop'] if 'loop' in anim else True
                self.animations[name] = Animation(imgs, anim['frame_time'], loop)
    
    def __getitem__(self, key):
        return self.config[key]
    
    def get_anim(self, id):
        return self.animations[id].copy()


class GameDataManager():
    def __init__(self, path):
        self._entities_data = read_json(join(path, 'entities.json'))
        self.sprites = {}
        self.load_sprites_data()
    
    def load_sprites_data(self):
        for id in self._entities_data:
            self.sprites[id] = SpriteData(self._entities_data[id])
