
from os.path import join
from json import load


WIN_SIZE = (800, 608)

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