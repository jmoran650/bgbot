from .minion import Minion

class Board():

    MAX_MINIONS = 7

    def __init__(self):
        self.minions = []
        self.hero = None
        self.hero_power = None
    
    def add_minion(self, minion: Minion):
        if len(self.minions) < self.MAX_MINIONS:
            self.minions.append(minion)
        else:
            raise ValueError("Board is full")
    
    def remove_minion(self, minion: Minion):
        if minion in self.minions:
            self.minions.remove(minion)
    
    def get_minions(self):
        return self.minions
    
    def get_minion_count(self):
        return len(self.minions)