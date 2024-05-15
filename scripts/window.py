
import pygame

from .core import SCREEN_SIZE


class Window():
    def __init__(self, caption='platformer', framerate=60):
        self.window = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(caption)
        
        self.clock = pygame.Clock()
        self.framerate = framerate
        self.dt = 0
        
        self.fps_font = pygame.font.SysFont('impact', 30)
        self.show_fps = False
    
    @property
    def fps(self):
        return self.clock.get_fps()

    def display_fps(self, state):
        self.show_fps = state
    
    def cycle(self, display, hud=None):
        self.window.blit(pygame.transform.scale(display, SCREEN_SIZE), (0, 0))
        
        if hud is not None:
            self.window.blit(hud, (0, 0))
        
        if self.show_fps:
            self.window.blit(self.fps_font.render(str(round(self.fps)), True, 'green'), (5, 3))
        
        self.dt = self.clock.tick(self.framerate)
        pygame.display.flip()
