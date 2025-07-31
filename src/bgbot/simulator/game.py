
from .player import Player
from .minion import Tribe
from .pool import Pool
class Game():
    def __init__(self):
        self.players = []
        self.tribes = []
        self.pool = Pool()
        self.game_state = "SETUP"

        def run_game(self):
            if self.game_state == "SETUP":
                # Initialize players, tribes, etc.
                self.game_state = "SHOP"
            
            while len(self.players) > 1:
                if self.game_state == "SHOP":
                    # AI logic for each player to buy/sell/roll
                    self.game_state = "COMBAT"
                
                elif self.game_state == "COMBAT":
                    # Pair players and simulate fights
                    # Remove defeated players
                    # if alive_players == 1: GAME_OVER
                    self.game_state = "SHOP"
            
