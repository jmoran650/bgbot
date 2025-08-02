# pool.py
"""
A simplified, shared pool of minions for all players in a game.
This refactored version uses a dataclass for type safety and clarity,
and simplifies the logic for rolling and managing minion counts.
"""
from __future__ import annotations
import random
from typing import Dict, List, Set
from dataclasses import dataclass, field
from .minion import Minion, Tribe

@dataclass(frozen=True)
class MinionData:
    """
    A dataclass to hold the static, unchanging blueprint for a minion.
    This avoids using "magic number" indices and provides type safety.
    """
    name: str
    tier: int
    attack: int
    health: int
    tribes: List[Tribe]
    keywords: list[str] = field(default_factory=lambda: [])
    effects: list[str] = field(default_factory=lambda: [])

# In a full implementation, this minion data would be loaded from a more robust
# data source like a JSON or YAML file.
ALL_MINIONS_DATA: list[MinionData] = [
    MinionData('Wrath Weaver', 1, 1, 3, [Tribe.DEMON]),
    MinionData('Vulgar Homunculus', 1, 2, 4, [Tribe.DEMON], ['Taunt']),
    MinionData('Micro Mummy', 1, 1, 2, [Tribe.MECH, Tribe.UNDEAD]),
    MinionData('Mecharoo', 1, 1, 1, [Tribe.MECH], ['Deathrattle']),
    MinionData('Scallywag', 1, 2, 1, [Tribe.PIRATE]),
    MinionData('Deckhand', 1, 2, 2, [Tribe.PIRATE]),
    MinionData('Sellemental', 1, 2, 2, [Tribe.ELEMENTAL]),
    MinionData('Refreshing Anomaly', 1, 1, 3, [Tribe.ELEMENTAL]),
    MinionData('Alleycat', 1, 1, 1, [Tribe.BEAST]),
    MinionData('Tabbycat', 1, 2, 1, [Tribe.BEAST]),
    MinionData('Murloc Tidecaller', 1, 1, 2, [Tribe.MURLOC]),
    MinionData('Murloc Tinyfin', 1, 1, 1, [Tribe.MURLOC]),
    MinionData('Dragonspawn Lieutenant', 1, 2, 3, [Tribe.DRAGON]),
    MinionData('Red Whelp', 1, 1, 2, [Tribe.DRAGON]),
    MinionData('Acolyte of CThun', 1, 2, 2, [Tribe.NEUTRAL], ['Taunt', 'Reborn']),
    MinionData('Micro Machine', 1, 1, 2, [Tribe.NEUTRAL]),
    MinionData('Manasaber', 2, 4, 2, [Tribe.BEAST]),
    MinionData('Scavenging Hyena', 2, 3, 2, [Tribe.BEAST]),
    MinionData('Annoy-o-Tron', 2, 1, 2, [Tribe.MECH], ['Taunt', 'Divine Shield']),
    MinionData('Harvest Golem', 2, 2, 3, [Tribe.MECH], ['Deathrattle']),
    MinionData('Rockpool Hunter', 2, 3, 2, [Tribe.MURLOC]),
    MinionData('Murloc Warleader', 2, 3, 3, [Tribe.MURLOC], ['Aura']),
    MinionData('Deck Swabbie', 2, 2, 3, [Tribe.PIRATE]),
    MinionData('Freedealing Gambler', 2, 3, 3, [Tribe.PIRATE]),
    MinionData('Imprisoner', 2, 3, 3, [Tribe.DEMON], ['Taunt', 'Deathrattle']),
    MinionData('Nathrezim Overseer', 2, 2, 4, [Tribe.DEMON], ['Battlecry']),
    MinionData('Harvest Sprite', 2, 3, 2, [Tribe.ELEMENTAL]),
    MinionData('Party Elemental', 2, 3, 3, [Tribe.ELEMENTAL], ['Aura']),
    MinionData('Glyph Guardian', 2, 3, 2, [Tribe.DRAGON]),
    MinionData('Steward of Time', 2, 2, 4, [Tribe.DRAGON], ['Aura']),
    MinionData('Rat Pack', 3, 2, 2, [Tribe.BEAST], ['Deathrattle']),
    MinionData('Monstrous Macaw', 3, 3, 3, [Tribe.BEAST], ['Trigger']),
    MinionData('Metaltooth Leaper', 3, 3, 3, [Tribe.MECH], ['Battlecry']),
    MinionData('Screwjank Clunker', 3, 4, 3, [Tribe.MECH], ['Battlecry']),
    MinionData('Soul Juggler', 3, 3, 5, [Tribe.DEMON], ['Aura']),
    MinionData('Floating Watcher', 3, 4, 4, [Tribe.DEMON]),
    MinionData('Cave Hydra', 4, 2, 4, [Tribe.BEAST], ['Cleave']),
    MinionData('Savannah Highmane', 4, 6, 5, [Tribe.BEAST], ['Deathrattle']),
    MinionData('Piloted Shredder', 4, 4, 3, [Tribe.MECH], ['Deathrattle']),
    MinionData('Security Rover', 4, 2, 6, [Tribe.MECH], ['Taunt', 'Summon']),
    MinionData('Ring Matron', 4, 6, 4, [Tribe.DEMON], ['Taunt', 'Deathrattle']),
    MinionData('Bigfernal', 4, 4, 4, [Tribe.DEMON], ['Scaling']),
    MinionData('Toxfin', 4, 2, 4, [Tribe.MURLOC], ['Battlecry']),
    MinionData('Felfin Navigator', 4, 4, 4, [Tribe.MURLOC], ['Battlecry']),
    MinionData('Goldgrubber', 4, 2, 2, [Tribe.PIRATE], ['Scaling']),
    MinionData('Southsea Strongarm', 4, 5, 4, [Tribe.PIRATE], ['Battlecry']),
    MinionData('Wildfire Elemental', 4, 6, 4, [Tribe.ELEMENTAL], ['Cleave']),
    MinionData('Majordomo Executus', 4, 5, 3, [Tribe.ELEMENTAL], ['Aura']),
    MinionData('Drakonid Enforcer', 4, 4, 5, [Tribe.DRAGON], ['Scaling']),
    MinionData('Cobalt Scalebane', 4, 5, 5, [Tribe.DRAGON], ['Aura']),
    MinionData('Mama Bear', 5, 5, 5, [Tribe.BEAST], ['Aura']),
    MinionData('Ironhide Direhorn', 5, 7, 7, [Tribe.BEAST], ['Summon']),
    MinionData('Foe Reaper 4000', 5, 6, 9, [Tribe.MECH], ['Cleave']),
    MinionData('Kangors Apprentice', 5, 3, 6, [Tribe.MECH], ['Deathrattle']),
    MinionData('Voidlord', 5, 3, 9, [Tribe.DEMON], ['Taunt', 'Deathrattle']),
    MinionData('MalGanis', 5, 9, 7, [Tribe.DEMON], ['Aura']),
    MinionData('King Bagurgle', 5, 6, 3, [Tribe.MURLOC], ['Deathrattle']),
    MinionData('Primalfin Lookout', 5, 3, 2, [Tribe.MURLOC], ['Battlecry']),
    MinionData('Capn Hoggarr', 5, 6, 6, [Tribe.PIRATE], ['Scaling']),
    MinionData('Seabreaker Goliath', 5, 8, 6, [Tribe.PIRATE], ['Windfury']),
    MinionData('Lieutenant Garr', 5, 8, 1, [Tribe.ELEMENTAL], ['Scaling']),
    MinionData('Nomi, Kitchen Nightmare', 5, 4, 4, [Tribe.ELEMENTAL], ['Aura']),
    MinionData('Razorgore, the Untamed', 5, 4, 6, [Tribe.DRAGON], ['Scaling']),
    MinionData('Murozond', 5, 5, 5, [Tribe.DRAGON], ['Battlecry']),
    MinionData('Ghastcoiler', 6, 7, 7, [Tribe.BEAST], ['Deathrattle']),
    MinionData('Goldrinn, the Great Wolf', 6, 4, 4, [Tribe.BEAST], ['Deathrattle']),
    MinionData('Omega Buster', 6, 6, 6, [Tribe.MECH], ['Deathrattle']),
    MinionData('Holy Mecherel', 6, 8, 4, [Tribe.MECH], ['Divine Shield']),
    MinionData('Imp Mama', 6, 6, 8, [Tribe.DEMON], ['Summon']),
    MinionData('Annihilan Battlemaster', 6, 3, 1, [Tribe.DEMON], ['Battlecry']),
    MinionData('Gentle Megasaur', 6, 5, 4, [Tribe.MURLOC], ['Battlecry']),
    MinionData('Felfin General', 6, 8, 6, [Tribe.MURLOC], ['Aura']),
    MinionData('Dread Admiral Eliza', 6, 6, 7, [Tribe.PIRATE], ['Aura']),
    MinionData('The Tide Razor', 6, 8, 4, [Tribe.PIRATE], ['Deathrattle']),
    MinionData('Lil Rag', 6, 4, 4, [Tribe.ELEMENTAL], ['Scaling']),
    MinionData('Amalgadon', 6, 6, 6, [Tribe.ELEMENTAL, Tribe.ALL], ['Battlecry']),
    MinionData('Kalecgos, Arcane Aspect', 6, 4, 12, [Tribe.DRAGON], ['Aura']),
    MinionData('Nadina the Red', 6, 7, 4, [Tribe.DRAGON], ['Deathrattle']),
]

# The number of copies of each minion, based on its Tavern Tier.
COPIES_PER_TIER: Dict[int, int] = {1: 15, 2: 15, 3: 13, 4: 11, 5: 9, 6: 7}

# --- Main Pool Class ---

class Pool:
    """
    A shared pool of minions from which all players draw. This class now
    separates the static minion blueprints (MinionData) from the dynamic
    game state (the counts of each minion).
    """

    def __init__(self, active_tribes: Set[Tribe]):
        """
        Initializes the minion pool for a new game.

        Args:
            active_tribes: A set of the Tribe enums active in this game.
        """
        # 1. Store the static, unchanging blueprint data for all minions in the game.
        self.minion_blueprints: Dict[str, MinionData] = {}

        # 2. Store the dynamic count of available minions. This is the only part
        #    of the pool that changes during the game.
        self.available_counts: Dict[str, int] = {}

        '''
        TO DO!
        
        '''
        active_tribes.add(Tribe.NEUTRAL) # Ensure neutral minions are always included

        for minion_data in ALL_MINIONS_DATA:
            # A minion is in the pool if any of its tribes are active, or if it's neutral.
            minion_tribes = set(minion_data.tribes) if minion_data.tribes else {Tribe.NEUTRAL}
            if not minion_tribes.isdisjoint(active_tribes):
                self.minion_blueprints[minion_data.name] = minion_data
                self.available_counts[minion_data.name] = COPIES_PER_TIER.get(minion_data.tier, 0)

    def roll(self, tavern_tier: int, num_to_roll: int) -> List[Minion]:
        """
        Generates a list of new Minion objects for a shop roll.

        Args:
            tavern_tier: The tavern tier of the player rolling.
            num_to_roll: The number of minions to generate for the shop.

        Returns:
            A list of new Minion objects.
        """
        # Get the names and counts of all minions that are both eligible by tier
        # and still have copies available in the pool.
        eligible_minions = {
            name: count
            for name, count in self.available_counts.items()
            if count > 0 and self.minion_blueprints[name].tier <= tavern_tier
        }

        if not eligible_minions:
            return []

        # Separate the names and their counts (weights) for the random.choices function.
        eligible_names = list(eligible_minions.keys())
        weights = list(eligible_minions.values())

        # Roll all minions at once. This is more efficient and correctly simulates
        # pulling from the pool without replacement for a single roll.
        # `k` is capped by the number of unique minions available to prevent errors.
        num_can_roll = min(num_to_roll, len(eligible_names))
        chosen_names = random.choices(eligible_names, weights=weights, k=num_can_roll)

        # Create Minion instances and decrement their counts from the pool.
        rolled_minions: List[Minion] = []
        for name in chosen_names:
            self.available_counts[name] -= 1
            blueprint = self.minion_blueprints[name]
        
            # Use the blueprint to construct a fresh Minion instance.
            rolled_minions.append(Minion(
                    name=blueprint.name,
                    tier=blueprint.tier,
                    attack=blueprint.attack,
                    health=blueprint.health,
                    tribes=blueprint.tribes,
                    keywords=blueprint.keywords
                ))
        return rolled_minions

    def return_minion(self, minion_name: str):
        """
        Increments the count of a minion in the pool when it's sold.

        Args:
            minion_name: The name of the minion being returned.
        """
        if minion_name in self.available_counts:
            blueprint = self.minion_blueprints[minion_name]
            max_copies = COPIES_PER_TIER.get(blueprint.tier, 0)
            
            if self.available_counts[minion_name] < max_copies:
                self.available_counts[minion_name] += 1
        else:
            # This can happen if a minion is generated by other means (e.g., hero power)
            # and was never officially part of the pool.
            print(f"Warning: Tried to return '{minion_name}', which is not in the pool's list.")

# --- Test Script ---
if __name__ == "__main__":
    print("--- Pool Test Script ---")

    # 1. Initialize the pool with some active tribes.
    active_game_tribes = {Tribe.MECH, Tribe.PIRATE, Tribe.DEMON}
    pool = Pool(active_tribes=active_game_tribes)
    print(f"Pool initialized with tribes: {active_game_tribes}\n")

    # 2. Define minions to track and print their initial counts.
    minions_to_watch = ['Scallywag', 'Micro Mummy', 'Annoy-o-Tron']
    print("--- Initial Counts ---")
    for name in minions_to_watch:
        print(f"  - {name}: {pool.available_counts.get(name, 0)}")

    # 3. Simulate a player at Tavern Tier 3 rolling the shop.
    print("\n--- Rolling Shop (Tier 3, 4 minions) ---")
    rolled_shop = pool.roll(tavern_tier=3, num_to_roll=4)
    print("Rolled:")
    if not rolled_shop:
        print("  (No minions were rolled)")
    else:
        for minion in rolled_shop:
            print(f"  - {minion.name} ({minion.attack}/{minion.health})")

    # 4. Print the counts again to see the decrease.
    print("\n--- Counts After Roll ---")
    for name in minions_to_watch:
        print(f"  - {name}: {pool.available_counts.get(name, 0)}")

    # 5. Simulate returning one of the rolled minions to the pool.
    if rolled_shop:
        minion_to_return = rolled_shop[0]
        print(f"\n--- Returning '{minion_to_return.name}' to the Pool ---")
        pool.return_minion(minion_to_return.name)

        # 6. Print the final counts to see the increase.
        print("\n--- Final Counts ---")
        for name in minions_to_watch:
            print(f"  - {name}: {pool.available_counts.get(name, 0)}")

    print("\n--- Test Complete ---")
