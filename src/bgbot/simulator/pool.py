"""pool.py
A simplified, shared pool of minions for all players in a game.
"""
import random
from typing import Dict, List, Any
from .minion import Minion, Tribe

<<<<<<< HEAD
'''
tier 1 : 15 copies
tier 2 : 15 copies
tier 3 : 13 copies
tier 4 : 11 copies
tier 5 : 9 copies
tier 6 : 7 copies

'''

class Pool(list[Tribe]):
=======
# In a full implementation, this minion data would be loaded from a more robust
# data source like a JSON or YAML file.
ALL_MINIONS_DATA = [
    {'name': 'Wrath Weaver', 'tier': 1, 'attack': 1, 'health': 3, 'tribes': [Tribe.DEMON]},
    {'name': 'Micro Mummy', 'tier': 1, 'attack': 1, 'health': 2, 'tribes': [Tribe.MECH, Tribe.UNDEAD]},
    {'name': 'Scallywag', 'tier': 1, 'attack': 2, 'health': 1, 'tribes': [Tribe.PIRATE]},
    {'name': 'Sellemental', 'tier': 1, 'attack': 2, 'health': 2, 'tribes': [Tribe.ELEMENTAL]},
    {'name': 'Manasaber', 'tier': 2, 'attack': 4, 'health': 2, 'tribes': [Tribe.BEAST]},
    {'name': 'Annoy-o-Tron', 'tier': 2, 'attack': 1, 'health': 2, 'tribes': [Tribe.MECH], 'keywords': ['Taunt', 'Divine Shield']},
    {'name': 'Patient Scout', 'tier': 3, 'attack': 1, 'health': 1, 'tribes': [], 'keywords': ['Discover']},
]

# The number of copies of each minion, based on its Tavern Tier.
COPIES_PER_TIER: Dict[int, int] = {1: 15, 2: 15, 3: 13, 4: 11, 5: 9, 6: 7}
>>>>>>> fbe42eb2dc49e16a82ab0ab4054dbdc0f5d46ba6

class Pool:
    """
    A shared pool of minion data from which all players draw.
    This class holds counts and stats, but not Minion objects.
    """

    def __init__(self, active_tribes: List[Tribe]):
        """
        Initializes the minion pool for a new game.

        Args:
            active_tribes: A list of the Tribe enums that are active in this game.
        """
        # The core data structure: {name: [count, tier, attack, health, tribes, keywords]}
        # A list is used to make the count mutable.
        self.minion_data: Dict[str, List[Any]] = {}

        if Tribe.NEUTRAL not in active_tribes:
            active_tribes.append(Tribe.NEUTRAL)

        for data in ALL_MINIONS_DATA:
            minion_tribes = data.get('tribes') or [Tribe.NEUTRAL]
            if any(tribe in active_tribes for tribe in minion_tribes):
                name = data['name']
                tier = data['tier']
                count = COPIES_PER_TIER.get(tier, 0)
                # Store all data needed to reconstruct the minion later.
                self.minion_data[name] = [
                    count,
                    tier,
                    data['attack'],
                    data['health'],
                    minion_tribes,
                    data.get('keywords', [])
                ]

    def roll(self, tavern_tier: int, count: int) -> List[Minion]:
        """
        Generates a list of new Minion objects for a shop roll, with chances
        weighted by the number of remaining copies.

        Args:
            tavern_tier: The tavern tier of the player rolling.
            count: The number of minions to roll for the shop.

        Returns:
            A list of new Minion objects.
        """
        # Get names and counts (weights) of minions that are eligible.
        eligible_minions = {
            name: data[0] for name, data in self.minion_data.items()
            if data[0] > 0 and data[1] <= tavern_tier
        }

        if not eligible_minions:
            return []
        
        # Separate names and their counts (weights) into parallel lists for random.choices.
        eligible_names = list(eligible_minions.keys())
        weights = list(eligible_minions.values())

        rolled_minions = []
        for _ in range(count):
            # If there are no minions left to choose (all weights are zero), stop.
            if not any(w > 0 for w in weights):
                break
            
            # Choose one minion based on the current weights.
            # random.choices returns a list, so we take the first element.
            chosen_name = random.choices(eligible_names, weights=weights, k=1)[0]
            
            # Find the index of the chosen minion to update its weight for the next pick.
            chosen_index = eligible_names.index(chosen_name)
            
            # Decrement the master count in the main data dictionary.
            self.minion_data[chosen_name][0] -= 1
            
            # Decrement the weight in our local list for the next iteration of this roll.
            weights[chosen_index] -= 1
            
            # Reconstruct a new Minion object from the stored data.
            data = self.minion_data[chosen_name]
            from .board import Board
            reconstructed_minion = Minion(
                name=chosen_name,
                board=Board(),
                attack=data[2],
                health=data[3],
                tribes=data[4],
                keywords=data[5]
            )
            rolled_minions.append(reconstructed_minion)
            
        return rolled_minions

    def return_minion(self, minion_name: str):
        """
        Increments the count of a minion in the pool when it's sold.

        Args:
            minion_name: The name of the minion being returned.
        """
        if minion_name in self.minion_data:
            data = self.minion_data[minion_name]
            tier = data[1]
            max_copies = COPIES_PER_TIER.get(tier, 0)
            
            # Increment count, ensuring it doesn't exceed the original maximum.
            if data[0] < max_copies:
                data[0] += 1
        else:
            print(f"Warning: Tried to return '{minion_name}', which is not in the pool.")
