
from os import listdir
from os.path import join
import pygame


def load_imgs(path, colorkey=None):
    imgs = []
    for name in listdir(path):
        surf = pygame.image.load(join(path, name))
        if colorkey:
            surf.set_colorkey(colorkey)
        imgs.append(surf)
    return imgs


class Animation():
    def __init__(self, images, frame_time, loop=True):
        self.images = images
        self.frames = len(self.images)
        self.frame_time = frame_time
        self.timer = 0
        self.loop = loop
        self.frame = 0
        self.paused = False
        self.done = False
        self.update(self.frame_time + 1)
    
    @property
    def img(self):
        return self.images[self.frame]
    
    def copy(self):
        return Animation(self.images, self.frame_time, self.loop)
    
    def update(self, dt):
        if not self.paused and not self.done:
            self.timer += dt
            if self.timer > self.frame_time:
                self.timer = 0
                self.frame += 1
                if self.frame == self.frames:
                    if self.loop:
                        self.rewind()
                    else:
                        self.end()
    
    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False
    
    def rewind(self):
        self.frame = 0
        self.done = False
    
    def end(self):
        self.done = True
        self.frame = self.frames - 1
