
import pygame
from sys import exit
pygame.init()

from scripts.scene import Scene
from scripts.gamedata import GameDataManager
from scripts.entity import Entity
import scripts.core as core


img1 = pygame.image.load('asset\\tile.png')
img2 = pygame.image.load('asset\\top.png')


class Game():
    def __init__(self):
        self.window = pygame.display.set_mode(core.WIN_SIZE)
        pygame.display.set_caption('platformer')
        self.clock = pygame.time.Clock()
        
        self.display = pygame.Surface(core.WIN_SIZE)
        
        self.data = GameDataManager()
        core.game = self
        
        self.map = Scene(core.asset('map.txt'))
        self.e = Entity('player', (400, 200))
    
    def quit(self):
        pygame.quit()
        exit()
    
    def get_events(self):
        self.dt = self.clock.tick(60)
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
                self.display.blit(img1, tile.rect)
            
            self.e.update()
            self.e.render(self.display)
            
            self.window.blit(self.display, (0, 0))
            
            pygame.display.flip()


if __name__ == '__main__':
    try:
        game = Game()
        game.run()
    except Exception as error:
        pygame.quit()
        raise error
