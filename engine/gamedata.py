
from os.path import join

from .core import read_json


class GameDataManager():
    def __init__(self, path):
        self.entities = read_json(join(path, 'entities.json'))
