
from os.path import join
import pygame
pygame.init()

import engine

from scripts.player import Player
from scripts.mob import Mob
from scripts.bullet import Bullet


class Game(engine.Game):
    def load(self):
        self.window.display_fps(True)
        
        self.asset.load_tileset('textures\\tiles\\tilebase')
        self.asset.load_tileset('textures\\tiles\\tileset_1')
        
        self.map = engine.Scene(join('asset\\', 'map.json'))
        self.cam.set_tilemap(self.map)
        
        self.player = Player((150, 50))
        self.entities.add(self.player)
        self.entities.add(Mob('None', (206, 70)))
        self.cam.focus(self.player)
    
    def update(self):
        self.inputs.process_events()
        if self.inputs.pressed(pygame.K_ESCAPE) or self.inputs.quit:
            self.quit()
        
        self.display.fill('deepskyblue3')
        
        if not self.player.alive and self.inputs.pressed(pygame.K_a):
            self.player.respawn((150, 50))
        
        if self.inputs.pressed(pygame.K_h):
            self.entities.add(Mob('None', (206, 70)))
        
        if self.inputs.pressed(pygame.K_g):
            self.actions.add(Bullet(self.player))
        elif self.inputs.pressed(pygame.K_UP):
            if self.inputs.holding(pygame.K_RIGHT):
                angle = 315
            elif self.inputs.holding(pygame.K_LEFT):
                angle = 225
            else:
                angle = 270
            self.actions.add(Bullet(self.player, angle=angle))

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
