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
ALL_MINIONS_DATA = [
    MinionData('Wrath Weaver', 1, 1, 3, [Tribe.DEMON]),
    MinionData('Micro Mummy', 1, 1, 2, [Tribe.MECH, Tribe.UNDEAD]),
    MinionData('Scallywag', 1, 2, 1, [Tribe.PIRATE]),
    MinionData('Sellemental', 1, 2, 2, [Tribe.ELEMENTAL]),
    MinionData('Manasaber', 2, 4, 2, [Tribe.BEAST]),
    MinionData('Annoy-o-Tron', 2, 1, 2, [Tribe.MECH], ['Taunt', 'Divine Shield']),
    MinionData('Patient Scout', 3, 1, 1, [Tribe.NEUTRAL], ['Discover']),
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
