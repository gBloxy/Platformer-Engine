
import pygame

from .core import read_file, TILE_SIZE


class Tile():
    __slots__ = ('gridx', 'gridy', 'pos', 'type', 'rect', 'void')
    def __init__(self, x, y, data):
        self.gridx = x
        self.gridy = y
        self.pos = (x * TILE_SIZE, y * TILE_SIZE)
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.type = data
        self.void = True if not self.type else False


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
                if int(tile):
                    t = Tile(x, y, tile)
                    self.map[y].append(t)
                    self.tiles.append(t)
                else:
                    self.map[y].append(None)
        
        self.rows = len(self.raw_map)
        self.cols = len(self.raw_map[0])
    
    def __getitem__(self, key):
        return self.map[key]
    
    def get_neighbors(self, pos, range_=1):
        neighbors = []
        
        for y in range(max(pos[1] - range_, 0), min(pos[1] + range_, self.rows)):
            for x in range(max(pos[0] - range_, 0), min(pos[0] + range_, self.cols)):
                tile = self.map[y][x]
                if not tile.void:
                    neighbors.append(tile)
        
        center = self.map[pos[1]][pos[0]]
        if not center.void:
            neighbors.remove(self.map[pos[1]][pos[0]])
        
        return neighbors
