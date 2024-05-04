
import pygame

from .core import read_file, TILE_SIZE


physics_types = {
    '0': 'air',
    '1': 'solid',
    '2': 'rampl',
    '3': 'rampr',
    '4': 'dropthrough'
}


class Tile():
    __slots__ = ('gridx', 'gridy', 'pos', 'type', 'rect', 'physics')
    def __init__(self, x, y, data):
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


class Scene():
    def __init__(self, file):
        data = read_file(file)
        
        self.raw_map = []
        self.map = []
        self.tiles = []
        
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
