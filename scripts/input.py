
import pygame


class Mouse():
    def __init__(self):
        self.pos = (0, 0)
        self.right = self.left = False
        self.holding_right = self.holding_left = False
        
    def update(self):
        self.right = self.left = False
        self.pos = pygame.mouse.get_pos()
    
    def process_down(self, event):
        if event.button == 1:
            self.left = True
            self.holding_left = True
        elif event.button == 3:
            self.right = True
            self.holding_right = True
    
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
