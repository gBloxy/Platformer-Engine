
import pygame
from sys import exit
pygame.init()

from scripts.scene import Scene
from scripts.gamedata import GameDataManager
from scripts.player import Player
from scripts.camera import Camera
import scripts.core as core


img1 = pygame.image.load('asset\\tile.png')
img2 = pygame.image.load('asset\\top.png')
font = pygame.font.SysFont('impact', 30)


class Game():
    def __init__(self):
        self.window = pygame.display.set_mode(core.WIN_SIZE)
        pygame.display.set_caption('platformer')
        self.clock = pygame.time.Clock()
        
        self.display = pygame.Surface((core.WIN_SIZE))
        
        self.dt = 0
        
        self.data = GameDataManager()
        core.game = self
        
        self.cam = Camera()
        self.map = Scene(core.asset('map.txt'))
        self.e = Player('player', (400, 200))
        self.cam.focus(self.e)
    
    def quit(self):
        pygame.quit()
        exit()
    
    def get_events(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_ESCAPE]:
            self.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
    
    def run(self):
        while True:
            self.get_events()
            
            self.display.fill('deepskyblue3')
            
            for tile in self.map.tiles:
                self.display.blit(img1, (tile.rect.x - self.cam.scroll[0], tile.rect.y - self.cam.scroll[1]))
            
            self.e.update()
            
            self.cam.update()
            
            self.e.render(self.display)
            
            self.window.blit(pygame.transform.scale(self.display, core.WIN_SIZE), (0, 0))
            
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
