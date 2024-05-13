
from sys import exit
from os.path import join
import pygame
pygame.init()

from scripts.window import Window
from scripts.scene import Scene
from scripts.gamedata import GameDataManager
from scripts.entity import PhysicEntity, EntityGroup
from scripts.player import Player
from scripts.camera import Camera
from scripts.input import Input
from scripts.asset import Assets
import scripts.core as core


class Game():
    def __init__(self):
        self.window = Window()
        self.window.display_fps(True)
        self.display = pygame.Surface(core.WIN_SIZE)
        
        core.game = self
        
        self.inputs = Input()
        self.mouse = self.inputs.mouse
        
        self.data = GameDataManager('asset\\')
        self.asset = Assets('asset\\')
        self.asset.load_imgs_folder('textures\\')
        
        self.map = Scene(self, join('asset\\', 'map.txt'))
        
        self.entities = EntityGroup()
        self.bullets = EntityGroup()
        self.cam = Camera(self, slowness=0.3)
        
        self.player = Player('player', (150, 50))
        self.entities.add(self.player)
        self.entities.add(PhysicEntity('player', (206, 70)))
        self.cam.focus(self.player)
    
    @property
    def dt(self):
        return self.window.dt

    def quit(self):
        pygame.quit()
        exit()
    
    def run(self):
        while True:
            self.inputs.process_events()
            if self.inputs.pressed(pygame.K_ESCAPE) or self.inputs.quit:
                self.quit()
            
            self.display.fill('deepskyblue3')
            
            self.cam.update()
            
            self.map.render(self.display, self.cam.scroll)
            
            self.entities.update(self.window.dt)
            self.entities.render(self.display, self.cam.scroll)
            
            if self.inputs.pressed(pygame.K_g):
                self.cam.screen_shake(5)
            
            self.bullets.update(self.window.dt)
            self.bullets.render(self.display, self.cam.scroll)
            
            self.window.cycle(self.display)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except Exception as error:
        pygame.quit()
        raise error
