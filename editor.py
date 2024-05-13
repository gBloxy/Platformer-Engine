
from tkinter import filedialog, messagebox, simpledialog
from os.path import join
from sys import exit
import pygame
pygame.init()

from scripts.core import TILE_SIZE, TILE_TUPLE, WIN_SIZE, SCREEN_SIZE, file_name, blit_center
from scripts.window import Window
from scripts.input import Input
from scripts.asset import Assets


SCALING = (SCREEN_SIZE[0] / WIN_SIZE[0], SCREEN_SIZE[1] / WIN_SIZE[1])

win = Window(caption='Platformer Engine - Editor')
inputs = Input()
mouse = inputs.mouse

display = pygame.Surface(WIN_SIZE)
gui = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

font = pygame.font.SysFont('arimo', 20)

depth_surf = pygame.Surface(TILE_TUPLE, pygame.SRCALPHA)
depth_surf.fill((0, 0, 0, 50))


def offset_rect(rect, scroll):
    return pygame.Rect(rect.x + scroll[0], rect.y + scroll[1], *rect.size)


def scale(pos):
    return (pos[0] * SCALING[0], pos[1] * SCALING[1])


class Button():
    def __init__(self, x, y, text, callback, icon=None, color=None):
        if icon is not None:
            img = pygame.transform.scale(pygame.image.load(join('editor_files', icon)), (25, 25))
            self.rect = pygame.Rect(x, y, 35, 35)
        else:
            img = font.render(text, True, 'black')
            self.rect = pygame.Rect(x, y, img.get_width() + 20, img.get_height() + 10)
        center = (self.rect.width/2, self.rect.height/2)
        self.img = pygame.Surface(self.rect.size)
        self.img.fill('gray')
        blit_center(self.img, img, center)
        self.img_hovered = pygame.Surface(self.rect.size)
        self.img_hovered.fill('lightgray')
        blit_center(self.img_hovered, img, center)
        if color:
            pygame.draw.rect(self.img, color, (0, 0, *self.rect.size), 2)
            pygame.draw.rect(self.img_hovered, color, (0, 0, *self.rect.size), 2)
        self.callback = callback
        self.hovered = False
    
    def update(self):
        if self.rect.collidepoint(mouse.real_pos):
            self.hovered = True
            if mouse.left:
                self.callback()
        else:
            self.hovered = False
    
    def render(self, surf):
        surf.blit(self.img_hovered if self.hovered else self.img, self.rect)


class ToggleButton():
    def __init__(self, x, y, callback, checked=True):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.img = pygame.Surface(self.rect.size)
        self.active = checked
        self.fill()
        self.callback = callback
        self.hovered = False
    
    def toggle(self):
        self.active = not self.active
        self.fill()
        self.callback()
    
    def fill(self):
        if self.active:
            self.img.fill('green')
        else:
            self.img.fill('red')
        pygame.draw.rect(self.img, 'black', (0, 0, *self.rect.size), 2)
    
    def update(self):
        if self.rect.collidepoint(mouse.real_pos):
            self.hovered = True
            if mouse.left:
                self.toggle()
        else:
            self.hovered = False
    
    def render(self, surf):
        surf.blit(self.img, self.rect)


class Assets(Assets):
    def __init__(self):
        super().__init__('')
        self.textures = {}
        self.images_alpha = {}
    
    def _load_img(self, path, data=None):
        surf = super()._load_img(path)
        name = file_name(path)
        self.textures[name] = pygame.transform.scale(surf, (30, 30))
        surf_alpha = surf.copy()
        surf_alpha.set_alpha(180)
        self.images_alpha[name] = surf_alpha
        
    def querry_load(self):
        path = filedialog.askdirectory()
        if path:
            self.load_imgs_folder(path)
        else:
            messagebox.showerror('Path Error', 'An error occured when choosing the textures path.')
    
    def clear(self):
        global selected
        self.images = {}
        self.textures = {}
        self.images_alpha = {}
        selected = None


class Selection():
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        
        self.x = min(pos1[0], pos2[0])
        self.y = min(pos1[1], pos2[1])
        self.width = max(pos1[0], pos2[0]) - self.x + 1
        self.height = max(pos1[1], pos2[1]) - self.y + 1
        
        self.tiles = []
        self.pastebin = {}
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                self.tiles.append((x, y))
                self.pastebin[(x - self.x, y - self.y)] = scene.get_at((x, y))[0]
    
    def set_pos2(self, pos):
        self.__init__(self.pos1, pos)
    
    def copy(self):
        return Selection(self.pos1, self.pos2)
    
    def render(self, surf):
        pygame.draw.rect(surf, 'blue', ((self.x * TILE_SIZE) + scroll[0], (self.y * TILE_SIZE) + scroll[1], self.width * TILE_SIZE, self.height * TILE_SIZE), 2)


class Scene():
    def __init__(self, data=None):
        self.layers = 3
        
        if data is not None:
            ...
        else:
            self.new_map()
        
        self.modified = False
    
    def new_map(self, dimension=(20, 10)):
        self.cols = dimension[0]
        self.rows = dimension[1]
        self.dim = [self.cols * TILE_SIZE, self.rows * TILE_SIZE]
        
        self.map = [[[['air', pygame.Rect((x*TILE_SIZE, y*TILE_SIZE), TILE_TUPLE)] for x in range(self.cols)] for y in range(self.rows)] for z in range(self.layers)]
        
        ind.set_modified('temp')
    
    def is_visible(self, tile):
        rect = tile[1]
        return not ( rect.bottom + scroll[1] < 0           or
                     rect.top    + scroll[1] > WIN_SIZE[1] or
                     rect.right  + scroll[0] < 0           or
                     rect.left   + scroll[0] > WIN_SIZE[0]   )
    
    def exist(self, pos):
        return 0 <= pos[0] < self.cols and 0 <= pos[1] < self.rows
    
    def hovered_pos(self):
        return (int(mouse_offseted[0] / TILE_SIZE), int(mouse_offseted[1] / TILE_SIZE))
    
    def set_at(self, pos, id):
        self.map[layer][pos[1]][pos[0]][0] = id
        self.modified = True
        ind.set_modified('modified')
    
    def get_at(self, pos):
        return self.map[layer][pos[1]][pos[0]]
    
    def remove(self, pos):
        self.set_at(pos, 'air')
    
    def remove_selection(self, selection):
        for pos in selection.tiles:
            self.remove(pos)
    
    def fill_selection(self, selection, tile_id):
        if tile_id is None:
            tile_id = 'air'
        for pos in selection.tiles:
            self.set_at(pos, tile_id)
    
    def paste_selection(self, tx, ty):
        if pastebin is not None:
            tiles = pastebin.pastebin
        else:
            return
        for x in range(pastebin.width):
            for y in range(pastebin.height):
                pos = (tx + x, ty + y)
                if self.exist(pos):
                    self.set_at(pos, tiles[(x, y)])
    
    def set_rows(self, rows):
        if rows == self.rows:
            return
        elif rows < self.rows:
            to_remove = self.rows - rows
            for y in range(to_remove):
                for z in range(3):
                    del self.map[z][-1]
        elif rows > self.rows:
            to_add = rows - self.rows
            for y in range(to_add):
                for z in range(3):
                    self.map[z].append([['air', pygame.Rect(x * TILE_SIZE, (y + self.rows) * TILE_SIZE, *TILE_TUPLE)] for x in range(self.cols)])
        self.rows = rows
        self.dim[1] = self.rows * TILE_SIZE
        self.modified = True
        ind.set_modified('modified')
    
    def set_cols(self, cols):
        if cols == self.cols:
            return
        elif cols < self.cols:
            to_remove = self.cols - cols
            for x in range(to_remove):
                for z in range(3):
                    for y in range(self.rows):
                        del self.map[z][y][-1]
        elif cols > self.cols:
            to_add = cols - self.cols
            for x in range(to_add):
                for z in range(3):
                    for y in range(self.rows):
                        self.map[z][y].append(['air', pygame.Rect((x + self.cols) * TILE_SIZE, y * TILE_SIZE, *TILE_TUPLE)])
        self.cols = cols
        self.dim[0] = self.cols * TILE_SIZE
        self.modified = True
        ind.set_modified('modified')


class Files():
    def __init__(self):
        self.path = None
    
    def save_scene(self):
        if self.path is None:
            self.path = filedialog.asksaveasfilename()
        scene.modified = False
    
    def check_modified(self):
        if scene.modified:
            if messagebox.askyesno(title='Save map', message='Current map as been modified\nSave current map ?', icon='warning'):
                self.save_scene()
    
    def new_scene(self):
        global scene
        self.check_modified()
        self.path = None
        scene = Scene()
    
    def open_scene(self):
        global scene
        self.check_modified()
        file = filedialog.askopenfilename()
        self.path = file
        scene = Scene(data=file)


class GUI():
    def __init__(self):
        self.buttons = []
        
        self.buttons.extend([
            Button(8, 50,  '', lambda: set_edit_mode('mouse'),  icon='cursor.png', color='black'),
            Button(8, 95,  '', lambda: set_edit_mode('place'),  icon='edit.png',   color='darkgreen'),
            Button(8, 140, '', lambda: set_edit_mode('select'), icon='select.png', color='blue'),
            Button(8, 185, '', lambda: set_edit_mode('remove'), icon='erase.png',  color='red'),
            Button(8, 230, '', self.toggle_layers, icon='layers.png'),
            Button(8, 275, '', files.new_scene,  icon='new.png'),
            Button(8, 320, '', files.open_scene, icon='open.png'),
            Button(8, 365, '', files.save_scene, icon='save.png'),
            Button(SCREEN_SIZE[0] - 43, 50, '', self.toggle_menu, icon='toggle_buttons.png')
        ])
        
        self.menu_btns = [
            Button(55,  50, 'Load textures', asset.querry_load),
            Button(210, 50, 'Clear', asset.clear),
            Button(290, 50, 'Resize x', self.resize_cols),
            Button(400, 50, 'Resize y', self.resize_rows),
            Button(510, 50, 'Center', scroll_to_center)
        ]
        
        x = SCREEN_SIZE[0] - 43
        self.selection_btns = [
            Button(x, 95,  '', copy_selection, icon='copy.png'),
            Button(x, 140, '', lambda: scene.paste_selection(selection.x, selection.y), icon='paste.png'),
            Button(x, 185, '', lambda: scene.fill_selection(selection, selected), icon='fill.png', color='darkgreen'),
            Button(x, 230, '', lambda: scene.remove_selection(selection), icon='cut.png',  color='red')
        ]
        
        y = 231
        self.layers_btns = [
            Button(83,  y, 'back', lambda: change_layer(0)),
            Button(190, y, 'main', lambda: change_layer(1)),
            Button(300, y, 'top',  lambda: change_layer(2)),
            ToggleButton(53,  y + 4, lambda: set_layer_visibility(0)),
            ToggleButton(160, y + 4, lambda: set_layer_visibility(1)),
            ToggleButton(270, y + 4, lambda: set_layer_visibility(2))
        ]
        
        self.active_menu = False
        self.active_selection = False
        self.active_layers = False
        self.toggle_menu()
    
    def toggle_menu(self):
        self.active_menu = not self.active_menu
        if self.active_menu:
            self.buttons.extend(self.menu_btns)
        else:
            for b in self.menu_btns:
                self.buttons.remove(b)
    
    def toggle_selection(self):
        self.active_selection = not self.active_selection
        if self.active_selection:
            self.buttons.extend(self.selection_btns)
        else:
            for b in self.selection_btns:
                self.buttons.remove(b)
    
    def toggle_layers(self):
        self.active_layers = not self.active_layers
        if self.active_layers:
            self.buttons.extend(self.layers_btns)
        else:
            for b in self.layers_btns:
                self.buttons.remove(b)
    
    def resize_rows(self):
        rows = simpledialog.askinteger('Resize map', 'Map rows number', minvalue=1)
        if rows is not None:
            scene.set_rows(rows)
    
    def resize_cols(self):
        cols = simpledialog.askinteger('Resize map', 'Map cols number', minvalue=1)
        if cols is not None:
            scene.set_cols(cols)
    
    def any_hovered(self):
        for b in self.buttons:
            if b.hovered:
                return True
        return False
    
    def update_render(self, surf):
        for b in self.buttons:
            b.update()
            b.render(gui)


class Indications():
    def __init__(self):
        self.right = SCREEN_SIZE[0] - 20
        self.centery = SCREEN_SIZE[1] - 30
        self.font = pygame.font.SysFont('arimo', 15)
        self.layers = {0:'back', 1:'main', 2:'top'}
        self.set_pos((0, 0))
        self.set_layer(1)
        self.set_modified('temp')
    
    def set_pos(self, pos):
        self.pos_surf = self.font.render(f'x: [{pos[0]}] y: [{pos[1]}]', True, 'black')
    
    def set_layer(self, layer):
        layer = self.layers[layer]
        self.layer_surf = self.font.render(f'layer: [{layer}]', True, 'black')
    
    def set_modified(self, state):
        self.state_surf = self.font.render('*'+state if state == 'modified' else state, True, 'black')
    
    def render(self, surf):
        right = self.right - self.pos_surf.get_width()
        surf.blit(self.pos_surf, (right, self.centery - self.pos_surf.get_height() / 2))
        right = right - self.layer_surf.get_width() - 8
        surf.blit(self.layer_surf, (right, self.centery - self.layer_surf.get_height() / 2))
        right = right - self.state_surf.get_width() - 8
        surf.blit(self.state_surf, (right, self.centery - self.state_surf.get_height() / 2))


def set_edit_mode(mode):
    global edit_mode, edit_color, selection, pos1, pos2
    edit_mode = mode
    if mode == 'mouse':
        edit_color = 'black'
    elif mode == 'place':
        edit_color = 'orange'
    elif mode == 'remove':
        edit_color = 'red'
    elif mode == 'select':
        edit_color = 'blue'
    if mode != 'select' and selection is not None:
        selection = pos1 = pos2 = None
        if btns.active_selection:
            btns.toggle_selection()


def change_layer(level):
    global layer
    layer = level
    ind.set_layer(level)


def copy_selection():
    global pastebin
    pastebin = selection.copy()


def scroll_to_center():
    global scroll
    x = int(scene.cols // 2) * TILE_SIZE
    y = int(scene.rows // 2) * TILE_SIZE
    scroll = [WIN_SIZE[0] // 2 - x, WIN_SIZE[1] // 2 - y]


def set_layer_visibility(level):
    layers[level] = not layers[level]


asset = Assets()
ind = Indications()
scene = Scene()
files = Files()
btns = GUI()

scroll = [20, 40]
tex_scroll = 0

moving_map = False
old_mouse_pos = (0, 0)

edit_mode = 'mouse'
selected = None
edit_color = 'orange'

selection = None
pos1 = pos2 = None
pastebin = None

layer = 1
layers = [True, True, True]


while True:
    # events
    inputs.process_events()
    if inputs.pressed(pygame.K_ESCAPE) or inputs.quit:
        pygame.quit()
        exit()
        # TODO : ask for save the map before quiting
    
    # clear all the render surfaces
    display.fill('deepskyblue3')
    gui.fill((0, 0, 0, 0))
    
    # check if mouse is hovering a menu element
    ui_hovered = btns.any_hovered()
    if mouse.real_pos[1] < 40:
        ui_hovered = True
    
    # move the map
    if (mouse.holding_right or inputs.holding(pygame.K_SPACE)) and not moving_map and not ui_hovered:
        moving_map = True
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    if moving_map:
        if not (mouse.holding_right or inputs.holding(pygame.K_SPACE)) or ui_hovered:
            moving_map = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        scroll[0] += (mouse.real_pos[0] - old_mouse_pos[0]) / SCALING[0]
        scroll[1] += (mouse.real_pos[1] - old_mouse_pos[1]) / SCALING[1]
    old_mouse_pos = mouse.real_pos
    
    # the mouse pos minus the scroll to get the tiles collisions without scroll issues
    mouse_offseted = (mouse.pos[0] - scroll[0], mouse.pos[1] - scroll[1])
    
    # check if the mouse is hovering the map
    if ui_hovered:
        mouse_in_map = False
    elif not (scroll[0] + 1 <= mouse.pos[0] <= scene.dim[0] + scroll[0] - 1):
        mouse_in_map = False
    elif not (scroll[1] + 1 <= mouse.pos[1] <= scene.dim[1] + scroll[1] - 1):
        mouse_in_map = False
    else:
        mouse_in_map = True
    
    if any(layers):
        # background grid
        for x in range(scene.cols + 1):
            posx = (x * TILE_SIZE + scroll[0]) * SCALING[0]
            pygame.draw.line(gui, 'lightgray', (posx, scroll[1] * SCALING[1]), (posx, (scroll[1] + scene.dim[1]) * SCALING[1]))
        for y in range(scene.rows + 1):
            posy = (y * TILE_SIZE + scroll[1]) * SCALING[0]
            pygame.draw.line(gui, 'lightgray', (scroll[0] * SCALING[0], posy), ((scroll[0] + scene.dim[0]) * SCALING[0], posy))
        # x and y axis
        pygame.draw.line(gui, 'red', scale(scroll), scale((scroll[0] + scene.dim[0], scroll[1])), 2)
        pygame.draw.line(gui, 'blue', scale(scroll), scale((scroll[0], scroll[1] + scene.dim[1])), 2)
    
    # texture choosing ui background
    pygame.draw.rect(gui, 'lightgray', (0, 0, SCREEN_SIZE[0], 40))
    
    # scroll between textures
    if mouse.real_pos[1] < 40:
        if mouse.scroll_up:
            tex_scroll -= 20
        elif mouse.scroll_down:
            tex_scroll += 20
    
    # update and render the textures choosing panel
    x = 10
    for name in asset.textures:
        pos = x + tex_scroll
        if -30 <= pos <= SCREEN_SIZE[0] + 30:
            rect = pygame.Rect(x + tex_scroll, 0, 40, 40)
            # hover texture
            if rect.collidepoint(mouse.real_pos):
                pygame.draw.rect(gui, 'gray', (rect.x - 5, rect.y, *rect.size))
                # select texture
                if mouse.left:
                    selected = name
                    set_edit_mode('place')
            # green background indicator
            if name == selected:
                pygame.draw.rect(gui, 'green', (rect.x - 5, rect.y, *rect.size))
            # render it
            gui.blit(asset.textures[name], (x + tex_scroll, 5))
        x += 45
    
    # manage buttons / indications
    btns.update_render(gui)
    ind.render(gui)
    
    # hovered tile
    if mouse_in_map:
        hovered = scene.hovered_pos()
        hovered_tile = scene.map[layer][hovered[1]][hovered[0]]
        ind.set_pos(hovered)
    
    # edit actions
    if mouse.left and not ui_hovered and mouse_in_map:
        if edit_mode == 'place' and selected is not None:
            scene.set_at(hovered, selected)
        elif edit_mode == 'remove':
            scene.remove(hovered)
        elif edit_mode == 'select':
            if selection is None:
                selection = Selection(hovered, hovered)
                pos1 = hovered
            elif pos2 is None:
                selection.set_pos2(hovered)
                pos2 = hovered
                btns.toggle_selection()
            else:
                selection = pos1 = pos2 = None
                btns.toggle_selection()
    
    # render tilemap
    for z, current_layer in enumerate(scene.map):
        for y, row in enumerate(current_layer):
            for x, tile in enumerate(row):
                if scene.is_visible(tile) and layers[z]:
                    rect = offset_rect(tile[1], scroll)
                    if tile[0] != 'air':
                        display.blit(asset[tile[0]], rect)
                        if z != layer:
                            display.blit(depth_surf, rect)
    
    # render hovered tile / actions indication
    if mouse_in_map and any(layers):
        rect = offset_rect(hovered_tile[1], scroll)
        if edit_mode == 'place':
            if selected is not None:
                display.blit(asset.images_alpha[selected], rect)
            else:
                pygame.draw.rect(display, edit_color, rect, 1)
        elif edit_mode != 'mouse':
            pygame.draw.rect(display, edit_color, rect, 1)
    
    # render tiles selection
    if selection is not None:
        selection.render(display)
    
    win.cycle(display, hud=gui)
