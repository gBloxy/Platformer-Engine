
from tkinter import filedialog, simpledialog
from os.path import join, dirname
from os import mkdir
import sys
import pygame
pygame.init()

sys.path.append(join(dirname(__file__), 'engine'))

from core import TILE_SIZE, TILE_TUPLE, blit_center, write_json, file_name
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


class Button():
    def __init__(self, x, y, callback, icon, color=None):
        img = pygame.transform.scale(pygame.image.load(join('editor_files', icon)), (25, 25))
        self.rect = pygame.Rect(x, y, 35, 35)
        center = (self.rect.width/2, self.rect.height/2)
        self.img = pygame.Surface(self.rect.size)
        self.img.fill('gray')
        blit_center(self.img, img, center)
        if color:
            pygame.draw.rect(self.img, color, (0, 0, *self.rect.size), 2)
        self.callback = callback
        self.hovered = False
    
    def update(self):
        if self.rect.collidepoint(mouse.real_pos):
            self.hovered = True
            if mouse.left:
                self.callback()
        else:
            self.hovered = False


def get_valid_name(title, content):
    name = simpledialog.askstring(title, content)
    if name is not None and name != '' and not name.isspace() and not any([c in name for c in invalid_chars]):
        return name
    else:
        return None


def get_physics():
    options = ['solid', 'air', 'rampr', 'rampl', 'dropthrough']
    value = input(f'Set tile physics type (options : {options} : ')
    if value in options:
        return value
    else:
        print('Wrong value !')
        return None


def save():
    data = {}
    for id in tiles:
        tile = tiles[id]
        if len(tile) == 3:
            data[id] = (tile[0], tile[2])
        else:
            data[id] = (tile[0],)
    save_path = dirname(path) + '/' + file_name(path) + '.json'
    write_json(save_path, data)
    print('Tileset data saved into configuration file at path : '+save_path)
    pygame.quit()
    sys.exit()


def set_index():
    global index
    i = simpledialog.askinteger('Tiles Index', 'Set the current tile id index :')
    if i:
        index = i


def export():
    folder_name = get_valid_name('Save', 'Set exported tiles folder name :')
    if folder_name:
        mkdir(folder_name)
        for name in tiles:
            surf = tileset.subsurface(tiles[name][0], tiles[name][1]).copy()
            pygame.image.save(surf, join(folder_name, name+'.png'))
        pygame.quit()
        sys.exit()


def same_pos(pos):
    for tile in tiles:
        if tiles[tile][0] == pos:
            return tile
    return None


hovered_surf = pygame.Surface(TILE_TUPLE, pygame.SRCALPHA)
pygame.draw.rect(hovered_surf, (255, 0, 0, 100), (0, 0, TILE_SIZE, TILE_SIZE))


buttons = [
    Button(SCREEN_SIZE[0] - 45, 10, save, 'save.png', color='green'),
    Button(SCREEN_SIZE[0] - 45, 55, set_index, 'list.png', color='orange'),
    Button(SCREEN_SIZE[0] - 45, 100, export, 'export.png', color='blue')
]

for b in buttons:
    gui.blit(b.img, b.rect)


pygame.time.wait(1000)

path = filedialog.askopenfilename()
if path:
    tileset = pygame.image.load(path)
else:
    pygame.quit()
    raise Exception('Need to open a tileset to run !')

tiles = {}
index = 1


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
    
    ui = False
    for b in buttons:
        b.update()
        if b.hovered:
            ui = True
    
    if not ui:
        hovered = (int(mouse.pos[0] / TILE_SIZE), int(mouse.pos[1] / TILE_SIZE))
        display.blit(hovered_surf, (hovered[0] * TILE_SIZE, hovered[1] * TILE_SIZE))
        
        if mouse.right or mouse.left or inputs.pressed(pygame.K_SPACE):
            
            pos = (hovered[0] * TILE_SIZE, hovered[1] * TILE_SIZE)
            same = same_pos(pos)
            
            if same is not None:
                
                if mouse.left:
                    tiles.pop(same)
                
                elif mouse.right:
                    physics = get_physics()
                    if physics:
                        if len(tiles[same]) == 3:
                            tiles[same][2] = physics
                        else:
                            tiles[same].append(physics)
                
                elif inputs.pressed(pygame.K_SPACE):
                    name = get_valid_name('Tile id', 'Set tile id :')
                    if name:
                        data = tiles[same]
                        tiles.pop(same)
                        tiles[name] = data
            
            else:
                if mouse.left or mouse.right:
                    name = 'tile_'+str(index)
                    index += 1
                    
                    if mouse.right:
                        physics = get_physics()
                        if physics:
                            tiles[name] = [pos, TILE_TUPLE, physics]
                    else:
                        tiles[name] = [pos, TILE_TUPLE]
                
                elif inputs.pressed(pygame.K_SPACE):
                    name = get_valid_name('Tile id', 'Set tile id :')
                    if name:
                        tiles[name] = [pos, TILE_TUPLE]
    
    for tile in tiles.values():
        pygame.draw.rect(display, 'blue' if len(tile) == 3 else 'green', (tile[0], tile[1]), 1)
    
    win.cycle(display, hud=gui)
