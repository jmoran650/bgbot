"""game.py
Main game logic for Hearthstone Battlegrounds simulator.
"""
import random
from .minion import Tribe
from .pool import Pool
from .tavern import Tavern
from .combat import Combat


def pick_random_tribes():
    """
    Randomly select 5 unique tribes from the Tribe enum.
    Returns a list of 5 Tribe members.
    """
    all_tribes = list(Tribe)
    return random.sample(all_tribes, 5)

class Game():
    
    def __init__(self, num_players: int = 4):
        
        ''' 
        Instantiate the game class to start a new battelgrounds
        games

        Args: 
            num_players: Number of players

        '''
        self.tribes = pick_random_tribes()
        self.pool = Pool(set(self.tribes))

        # Create taverns with players - each tavern owns its player
        self.taverns = []

        # we need to instantiate taverns and players for the number of players in the game
        # for our taverns all we need is to pass in the pool
        # for our players all we need is to pass in is a unique name and hero

        hero_names = ["Reno", "Flurgl", "Patches", "Millhouse", "Galewing", "Lich King", "Rafaam", "Toki"]


        for players in range(num_players):
            # instantiates taverns for however many players are in the game
            tavern = Tavern(self.pool)
            #
            tavern.player.name = f"player {players + 1}"
            tavern.player.hero = hero_names[players % len(hero_names)]
            self.taverns.append(tavern)


        self.turn = 1
        self.game_state = "SHOP"
        
        print(f"=== BATTLEGROUNDS GAME STARTED ===")
        print(f"Players: {num_players}")
        print(f"Active tribes: {[t.value for t in self.tribes]}")
        print()
            



print(range(5))


    # def __init__(self):
    #     self.players = []
    #     self.tribes = []
    #     self.tribes = pick_random_tribes()
    #     self.pool = Pool(self.tribes)
    #     self.game_state = "SETUP"

    # def run_game(self):
    #     if self.game_state == "SETUP":
    #         # Initialize players, tribes, etc.
    #         self.game_state = "SHOP"
        
    #     while len(self.players) > 1:
    #         if self.game_state == "SHOP":
    #             # AI logic for each player to buy/sell/roll
    #             self.game_state = "COMBAT"
            
    #         elif self.game_state == "COMBAT":
    #             # Pair players and simulate fights
    #             # Remove defeated players
    #             # if alive_players == 1: GAME_OVER
    #             self.game_state = "SHOP"
            
