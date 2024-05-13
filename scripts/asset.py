
import pygame
from os import listdir
from os.path import join

from .core import file_name, read_json


class Assets():
    def __init__(self, asset_path):
        self.path = asset_path
        self.images = {}
        self.sounds = {}
    
    def __getitem__(self, key):
        return self.images.get(key, self.sounds.get(key))
    
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
    
    def load_sound(self, path, volume=1):
        sound = pygame.mixer.Sound(join(self.path, path))
        sound.set_volume(volume)
        self.sounds[file_name(path)] = sound
    
    def load_sounds_folder(self, path, volumes):
        for name in listdir(join(self.path, path)):
            self.load_sound(join(self.path, path, name), volumes[file_name(name)])
