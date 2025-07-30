from .board import Board
from .minion import Minion
from .player import Player

class Tavern:
    def __init__(self):
        self.shop = []
        self.hand = []
        self.tavernBoard = Board()
        self.player = Player()

    # Roll: Call pool to get minions, set shop equal to pool.roll result
        # SOMETIMES ROLLS ARE FREE OR HAVE SPECIAL PROPERTIES I.E ALL BEING OF ONE MINION TYPE ETC

    # Freeze: idk

    # Tavern Tier: Gold check, then increment tavern tier by one


