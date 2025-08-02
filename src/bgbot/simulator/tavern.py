from __future__ import annotations
from typing import TYPE_CHECKING, List, Dict
import logging

if TYPE_CHECKING:
    from .minion import Minion
    from .player import Player
    from .pool import Pool


class Tavern:
    """Manages the player's shop, including minions, rolls, and tier upgrades."""

    # Official shop size based on Tavern Tier
    SHOP_SIZE_BY_TIER: Dict[int, int] = {
        1: 3, 2: 4, 3: 4, 4: 5, 5: 5, 6: 6
    }
    # Official costs to upgrade to the next tier
    UPGRADE_COSTS: Dict[int, int] = {
        2: 5, 3: 7, 4: 8, 5: 10, 6: 10
    }

    def __init__(self, owner: Player, pool: Pool):
        self.shop: List[Minion] = []
        self.hand = []
        self.owner = owner
        self.pool = pool
        self.tier: int = 1
        self.is_frozen = False
        # The cost to upgrade to tier 2 starts at 5 and is reduced by 1 each turn.
        self.upgrade_cost: int = self.UPGRADE_COSTS.get(2, 5)

    def start_of_turn_refresh(self) -> None:
        """
        Handles the automatic shop refresh at the start of a turn.
        If the shop was frozen, it unfreezes it. Otherwise, it rolls a new shop.
        """
        if self.is_frozen:
            self.is_frozen = False  # Unfreeze for the next turn
            logging.info(f"    Shop was frozen, now available for {self.owner.name}.")
        else:
            self._reroll()

    def reroll_shop(self) -> None:
        """Handles a paid reroll, which always provides a new shop."""
        self._reroll()

    def _reroll(self) -> None:
        """Internal logic to return old minions and get a new shop from the pool."""
        self._return_shop_to_pool()
        count = self.SHOP_SIZE_BY_TIER.get(self.tier, 6)  # Default to 6 for safety
        self.shop = self.pool.roll(self.tier, count)

    def _return_shop_to_pool(self) -> None:
        """Returns all minions currently in the shop back to the shared pool."""
        for minion in self.shop:
            self.pool.return_minion(minion.name)
        self.shop = []

    def freeze(self) -> None:
        """Freezes the current shop to keep it for the next turn."""
        self.is_frozen = True

    def upgrade_tavern(self) -> None:
        """Upgrades the tavern to the next tier and sets the cost for the next level."""
        if self.tier < 6:
            self.tier += 1
            # Set the base cost for the *next* upgrade
            self.upgrade_cost = self.UPGRADE_COSTS.get(self.tier + 1, 0)
            logging.info(f"    Tavern is now Tier {self.tier}.")

    def reduce_upgrade_cost(self) -> None:
        """Reduces the upgrade cost by 1 (called once per turn)."""
        if self.upgrade_cost > 0:
            self.upgrade_cost -= 1

    def display_shop(self):
        """logging.infos the current contents of the shop."""
        if not self.shop:
            logging.info("    Shop is empty!")
            return
        shop_str = ", ".join(f"{m.name}({m.attack}/{m.health})" for m in self.shop)
        logging.info(f"    Shop: [{shop_str}]")