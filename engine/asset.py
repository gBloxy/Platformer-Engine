
import pygame
from os import listdir
from os.path import join, dirname

from engine.core import file_name, read_json, TILE_TUPLE
import engine.scene as scene


class Assets():
    def __init__(self, asset_path):
        self.path = asset_path
        self.images = {}
        self.sounds = {}
    
    def __getitem__(self, key):
        return self.images[key]
    
    def _load_img(self, path, data=None):
        surf = pygame.image.load(path)
        self.images[file_name(path)] = surf
        return surf
    
    def load_img(self, path, data_file=None):
        if data_file:
            data = read_json(data_file)
        self._load_img(join(self.path, path), data)
    
    def load_imgs_folder(self, path, data_file=None):
        if data_file:
            data = read_json(data_file)
        for name in listdir(join(self.path, path)):
            self._load_img(join(self.path, path, name), data if data_file else None)
    
    def load_tileset(self, path):
        data = read_json(join(self.path, path) + '.json')
        tileset = pygame.image.load(join(self.path, dirname(path), file_name(path))+'.png')
        tiles = {}
        for id in data:
            tile = data[id]
            surf = tileset.subsurface(tile[0], TILE_TUPLE).copy()
            tiles[id] = surf
            if len(tile) == 2:
                physics_type = tile[1]
                scene.physics_types[id] = physics_type
        self.images.update(tiles)
        return tiles
    
    def load_sound(self, path, volume=1):
        sound = pygame.mixer.Sound(join(self.path, path))
        sound.set_volume(volume)
        self.sounds[file_name(path)] = sound
    
    def load_sounds_folder(self, path, volumes):
        for name in listdir(join(self.path, path)):
            self.load_sound(join(self.path, path, name), volumes[file_name(name)])
    
    def play(self, sound):
        self.sounds[sound].play()
