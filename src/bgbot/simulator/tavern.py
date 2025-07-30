from .board import Board
from .minion import Minion
from .player import Player

class Tavern:
    def __init__(self):
        self.shop = []
        self.hand = []
        self.tavernBoard = Board()
        self.player = Player()
