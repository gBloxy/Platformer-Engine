
from os.path import join
import pygame
pygame.init()

import engine

from scripts.player import Player
from scripts.mob import Mob


class Game(engine.Game):
    def load(self):
        self.window.display_fps(True)
        
        self.asset.load_imgs_folder('textures\\')
        
        self.map = engine.Scene(join('asset\\', 'map.txt'))
        self.cam.set_tilemap(self.map)
        
        self.player = Player('player', (150, 50))
        self.entities.add(self.player)
        self.entities.add(Mob((206, 70)))
        self.cam.focus(self.player)
    
    def update(self):
        self.inputs.process_events()
        if self.inputs.pressed(pygame.K_ESCAPE) or self.inputs.quit:
            self.quit()
        
        self.display.fill('deepskyblue3')
        
        if self.inputs.pressed(pygame.K_g):
            self.cam.screen_shake(5)
        
        if self.inputs.pressed(pygame.K_h):
            self.entities.add(Mob((206, 70)))
        
        self.cam.update()
        
        self.map.render(self.display, self.cam.scroll)
        
        self.entities.update(self.window.dt)
        self.entities.render(self.display, self.cam.scroll)
        
        self.actions.update(self.window.dt)
        self.actions.render(self.display, self.cam.scroll)
        
        self.window.cycle(self.display)


if __name__ == '__main__':
    try:
        game = Game(asset_path='asset\\')
        game.run()
    except Exception as error:
        pygame.quit()
        raise error
