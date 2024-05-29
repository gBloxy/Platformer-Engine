
from tkinter import filedialog, simpledialog
from os.path import join, dirname
from os import mkdir
import sys
import pygame
pygame.init()

sys.path.append(join(dirname(__file__), 'engine'))

from core import TILE_SIZE, TILE_TUPLE, file_name, blit_center, write_json, read_json
from window import Window
from input import Input


SCREEN_SIZE = (900, 600)
WIN_SIZE = (300, 200)

SCALING = (SCREEN_SIZE[0] / WIN_SIZE[0], SCREEN_SIZE[1] / WIN_SIZE[1])

win = Window(SCREEN_SIZE, caption='Platformer Engine - Tileset Handler')
inputs = Input(SCREEN_SIZE, WIN_SIZE)
mouse = inputs.mouse

display = pygame.Surface(WIN_SIZE)
gui = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)


invalid_chars = ['/', '\\', '*', '?', '"', '<', '>', '|']

cols = int(WIN_SIZE[0] / TILE_SIZE)
rows = int(WIN_SIZE[1] / TILE_SIZE)

hovered_surf = pygame.Surface(TILE_TUPLE, pygame.SRCALPHA)
pygame.draw.rect(hovered_surf, (255, 0, 0, 100), (0, 0, TILE_SIZE, TILE_SIZE))

save_icon = pygame.transform.scale(pygame.image.load(join('editor_files', 'save.png')), (40, 40))
save_rect = pygame.Rect(SCREEN_SIZE[0] - save_icon.get_width() - 10, 10, 40, 40)
pygame.draw.rect(gui, 'darkgray', save_rect)
gui.blit(save_icon, save_rect.topleft)


def get_valid_name(title, content):
    name = simpledialog.askstring(title, content)
    if name != '' and not name.isspace() and not any([c in name for c in invalid_chars]):
        return name
    else:
        return None


def save(folder_name):
    mkdir(folder_name)
    for name in tiles:
        pygame.image.save(tiles[name], join(folder_name, name+'.png'))


pygame.time.wait(1000)

path = filedialog.askopenfilename()
if path:
    tileset = pygame.image.load(path)
else:
    pygame.quit()
    raise Exception('Need to open a tileset to run.')

tiles = {}


while True:
    inputs.process_events()
    if inputs.quit or inputs.pressed(pygame.K_ESCAPE):
        pygame.quit()
        sys.exit()
    
    display.fill('white')
    
    display.blit(tileset, (0, 0))
    
    for x in range(cols+1):
        pygame.draw.line(display, 'black', (x * TILE_SIZE, 0), (x * TILE_SIZE, WIN_SIZE[1]))
    for y in range(rows+1):
        pygame.draw.line(display, 'black', (0, y * TILE_SIZE), (WIN_SIZE[0], y * TILE_SIZE))
    
    if save_rect.collidepoint(mouse.real_pos):
        ui = True
    else:
        ui= False
    
    if not ui:
        hovered = (int(mouse.pos[0] / TILE_SIZE), int(mouse.pos[1] / TILE_SIZE))
        display.blit(hovered_surf, (hovered[0] * TILE_SIZE, hovered[1] * TILE_SIZE))
        
        if mouse.left:
            name = get_valid_name('Tile id', 'Set the tile id.')
            if name is not None:
                tile = tileset.subsurface((hovered[0] * TILE_SIZE, hovered[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)).copy()
                tiles[name] = tile
    
    elif mouse.left:
        name = get_valid_name('Save', 'Set save folder name.')
        if name:
            save(name)
            pygame.quit()
            sys.exit()
    
    win.cycle(display, hud=gui)
