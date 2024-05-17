
import pygame

from engine import Element
from .core import read_file, TILE_SIZE, offset


physics_types = {
    '0': 'air',
    '1': 'solid',
    '2': 'rampl',
    '3': 'rampr',
    '4': 'dropthrough'
}


class Tile(Element):
    __slots__ = ('gridx', 'gridy', 'pos', 'type', 'rect', 'physics')
    def __init__(self, x, y, data):
        super().__init__()
        self.gridx = x
        self.gridy = y
        self.pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.type = data
        try:
            self.physics = physics_types[data]
        except:
            self.physics = 'air'
    
    @property
    def air(self):
        return self.physics == 'air'
    
    def is_visible(self, scroll):
        return not ( self.rect.bottom - scroll[1] < 0                 or
                     self.rect.top - scroll[1] > self.g.window.size[1]  or
                     self.rect.right - scroll[0] < 0                  or
                     self.rect.left - scroll[0] > self.g.window.size[0]   )


class Scene(Element):
    def __init__(self, file):
        super().__init__()
        self.raw_map = []
        self.map = []
        self.tiles = []
        
        data = read_file(file)
        
        for y, row in enumerate(data.splitlines()):
            self.raw_map.append([])
            self.map.append([])
            for x, tile in enumerate(row):
                self.raw_map[y].append(int(tile))
                if tile != '0':
                    t = Tile(x, y, tile)
                    self.map[y].append(t)
                    self.tiles.append(t)
                else:
                    self.map[y].append(Tile(x, y, '0'))
        
        self.rows = len(self.raw_map)
        self.cols = len(self.raw_map[0])
        self.width = self.cols * TILE_SIZE
        self.height = self.rows * TILE_SIZE
    
    def __getitem__(self, key):
        return self.map[key]
    
    def get_neighbors(self, pos, range_=1):
        neighbors = []
        
        for y in range(max(pos[1] - range_, 0), min(pos[1] + range_ + 1, self.rows)):
            for x in range(max(pos[0] - range_, 0), min(pos[0] + range_ + 1, self.cols)):
                tile = self.map[y][x]
                if not tile.air:
                    neighbors.append(tile)
        
        return neighbors
    
    def render(self, surf, scroll):
        for tile in self.tiles:
            if tile.is_visible(scroll):
                if tile.type == '1':
                    surf.blit(self.g.asset['tile'], offset(tile.rect.topleft, scroll))
                elif tile.type == '2':
                    surf.blit(self.g.asset['rampr'], offset(tile.rect.topleft, scroll))
                elif tile.type == '3':
                    surf.blit(self.g.asset['rampl'], offset(tile.rect.topleft, scroll))
                elif tile.type == '4':
                    surf.blit(self.g.asset['dropthrough'], offset(tile.rect.topleft, scroll))
                else:
                    surf.blit(self.g.asset['unknowed'], offset(tile.rect.topleft, scroll))
