
import pygame
from os.path import join
from json import load


WIN_SIZE = (800, 600)

TILE_SIZE = 32
TILE_TUPLE = (TILE_SIZE, TILE_SIZE)


game = None # main game class instance


def read_file(path):
    with open(path) as file:
        data = file.read()
    return data


def read_json(path):
    with open(path) as file:
        data = load(file)
    return data


def asset(path):
    return join('asset', path)


def clamp(value, minimum, maximum):
    return min(maximum, max(minimum, value))


def data():
    return game.data


def offset(pos, scroll):
    return (pos[0] - scroll[0], pos[1] - scroll[1])


def offset_rect(rect, scroll):
    return pygame.Rect(rect.x - scroll[0], rect.y - scroll[1], *rect.size)