
import pygame

from .core import WIN_SIZE, SCREEN_SIZE


class Mouse():
    def __init__(self):
        self.pos = (0, 0)
        self.real_pos = (0, 0)
        self.right = self.left = False
        self.holding_right = self.holding_left = False
        self.scroll_up = self.scroll_down = False
        self.scale_factor = (SCREEN_SIZE[0] / WIN_SIZE[0], SCREEN_SIZE[1] / WIN_SIZE[1])
    
    def world_pos(self, scroll):
        return (self.pos[0] + scroll[0], self.pos[1] + scroll[1])
        
    def update(self):
        self.right = self.left = False
        self.scroll_up = self.scroll_down = False
        self.real_pos = pygame.mouse.get_pos()
        self.pos = tuple(co / factor for co, factor in zip(self.real_pos, self.scale_factor))
    
    def process_down(self, event):
        if event.button == 1:
            self.left = True
            self.holding_left = True
        elif event.button == 3:
            self.right = True
            self.holding_right = True
        elif event.button == 4:
            self.scroll_up = True
            self.scrolling_up = True
        elif event.button == 5:
            self.scroll_down = True
            self.scrolling_down = True
    
    def process_up(self, event):
        if event.button == 1:
            self.holding_left = False
        elif event.button == 3:
            self.holding_right = False


class Input():
    def __init__(self):
        self.mouse = Mouse()
        self.keys_pressed = []
        self.keys_pressing = []
        self.keys_released = []
        self.quit = False
    
    def process_events(self):
        events = pygame.event.get()
        
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.mouse.update()
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.keys_pressed.append(e.key)
                self.keys_pressing.append(e.key)
            
            elif e.type == pygame.KEYUP:
                self.keys_pressing.remove(e.key)
                self.keys_released.append(e.key)
            
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.mouse.process_down(e)
            
            elif e.type == pygame.MOUSEBUTTONUP:
                self.mouse.process_up(e)
            
            elif e.type == pygame.QUIT:
                self.quit = True
        
    def pressed(self, key):
        return key in self.keys_pressed
    
    def holding(self, key):
        return key in self.keys_pressing
    
    def released(self, key):
        return key in self.keys_released
    
    def any_pressed(self):
        return bool(self.keys_pressed)
    
    def any_holding(self):
        return bool(self.keys_pressing)
    
    def any_released(self):
        return bool(self.keys_released)
