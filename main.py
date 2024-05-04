
import pygame
from sys import exit
pygame.init()

from scripts.scene import Scene
from scripts.gamedata import GameDataManager
from scripts.player import Player
from scripts.camera import Camera
from scripts.input import Input
import scripts.core as core


tile_img = pygame.image.load('asset\\tile.png')
rampr = pygame.image.load('asset\\rampr.png')
rampl = pygame.image.load('asset\\rampl.png')
dropthrough = pygame.image.load('asset\\dropthrough.png')
unknowed = pygame.image.load('asset\\unknowed.png')
font = pygame.font.SysFont('impact', 30)


class Game():
    def __init__(self):
        self.window = pygame.display.set_mode(core.SCREEN_SIZE)
        pygame.display.set_caption('platformer')
        self.clock = pygame.time.Clock()
        
        self.display = pygame.Surface(core.WIN_SIZE)
        
        self.dt = 0
        self.inputs = Input()
        self.mouse = self.inputs.mouse
        
        self.data = GameDataManager()
        core.game = self
        
        self.map = Scene(core.asset('map.txt'))
        self.player = Player('player', (150, 50))
        self.cam = Camera(self, slowness=0.3)
        self.cam.focus(self.player)
    
    def quit(self):
        pygame.quit()
        exit()
    
    def run(self):
        while True:
            self.inputs.process_events()
            if self.inputs.pressed(pygame.K_ESCAPE) or self.inputs.quit:
                self.quit()
            
            self.display.fill('deepskyblue3')
            
            for tile in self.map.tiles:
                if tile.type == '1':
                    self.display.blit(tile_img, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
                elif tile.type == '2':
                    self.display.blit(rampr, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
                elif tile.type == '3':
                    self.display.blit(rampl, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
                elif tile.type == '4':
                    self.display.blit(dropthrough, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
                else:
                    self.display.blit(unknowed, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
            
            self.player.update()
            
            self.cam.update()
            
            self.player.render(self.display)
            
            self.window.blit(pygame.transform.scale(self.display, core.SCREEN_SIZE), (0, 0))
            
            self.window.blit(font.render(str(round(self.clock.get_fps())), True, 'green'), (5, 3))
            
            pygame.display.flip()
            
            self.dt = self.clock.tick(60)


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except Exception as error:
        pygame.quit()
        raise error
