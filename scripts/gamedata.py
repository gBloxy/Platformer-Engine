
from .core import read_json, asset


class GameDataManager():
    def __init__(self):
        self.entities = read_json(asset('entities.json'))
