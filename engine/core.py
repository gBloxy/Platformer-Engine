
from os.path import basename, splitext
from json import load, dump
import pygame


TILE_SIZE = 16
TILE_TUPLE = (TILE_SIZE, TILE_SIZE)


def file_name(path):
    return splitext(basename(path))[0]


def relative_path(full_path, sub_path):
    return full_path[full_path.find(sub_path):] if sub_path in full_path else None


def read_file(path):
    with open(path) as file:
        data = file.read()
    return data


def read_json(path):
    with open(path) as file:
        data = load(file)
    return data


def write_file(path, data):
    with open(path, 'w') as file:
        file.write(data)


def write_json(path, data):
    with open(path, 'w') as file:
        dump(data, file)


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


def offset(pos, scroll):
    return (pos[0] - scroll[0], pos[1] - scroll[1])


def offset_rect(rect, scroll):
    return pygame.Rect(rect.x - scroll[0], rect.y - scroll[1], *rect.size)


def smooth(val, target, dt, slowness=1):
    val += (target - val) / slowness * min(dt / 1000, slowness)
    return val


def blit_center(target_surf, surf, pos):
    target_surf.blit(surf, (pos[0] - surf.get_width() / 2, pos[1] - surf.get_height() / 2))
