
import pygame
from sys import exit

from .window import Window
from .input import Input
from .gamedata import GameDataManager
from .asset import Assets
from .camera import Camera
from .entity import EntityGroup

import engine


class Game():
    def __init__(self, asset_path, cam_slowness=0.3, win_size=(900, 600), display_size=(450, 300), caption='Platformer', framerate=60):
        engine.g = self
        
        self.window = Window(win_size, caption, framerate)
        
        self.display = pygame.Surface(display_size)
        self.size = display_size
        
        self.inputs = Input()
        self.mouse = self.inputs.mouse
        
        self.asset = Assets(asset_path)
        self.data = GameDataManager(asset_path)
        
        self.cam = Camera(slowness=cam_slowness)
        
        self.entities = EntityGroup()
        self.actions = EntityGroup()
    
    @property
    def dt(self):
        return self.window.dt
    
    @property
    def dts(self):
        return self.window.dt / 100#0
    
    @property
    def win_size(self):
        return self.window.size

    def quit(self):
        pygame.quit()
        exit()
    
    def load(self):
        pass
    
    def update(self):
        self.inputs.process_events()
        if self.inputs.pressed(pygame.K_ESCAPE) or self.inputs.quit:
            self.quit()
        
        self.window.cycle(self.display)
    
    def run(self):
        self.load()
        while True:
            self.update()
