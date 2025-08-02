from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .minion import Minion
    from .player import Player
    from .pool import Pool


class Tavern:
    def __init__(self, owner:Player, pool: Pool):
        self.shop : list[Minion] = []
        self.hand = []
        self.owner = owner
        self.pool = pool
        self.tier: int = 1
        self.is_frozen = False

    # why is the count hardcoded crying emoji
    def roll(self, count: int = 3) -> None:
        """
        Roll for new minions in the shop.
        
        Args:
            count: Number of minions to roll for (default 3)
        """
        # Return current shop minions to pool before rolling
        self._return_shop_to_pool()
        
        # Get new minions from pool
        new_shop = self.pool.roll(self.tier, count)
        self.shop = new_shop

    def _return_shop_to_pool(self) -> None:
        """Return current shop minions back to the pool."""
        for minion in self.shop:
            self.pool.return_minion(minion.name)
        self.shop = []

    def freeze(self) -> None:
        """Freeze the current shop (keep it for next turn)."""
        # In a real implementation, you'd set a freeze flag
        # For now, we'll just keep the shop as-is
        self.is_frozen = True


    def upgrade_tavern(self) -> bool:
        """
        Attempt to upgrade tavern tier.
        
        Returns:
            True if upgrade was successful, False if not enough gold
        """
        # This would check player's gold and increment tier
        # For now, just increment the tier
        if self.tier < 6:
            self.tier += 1
            return True
        return False

    def display_shop(self):
        """Return a formatted string representing the current shop contents."""
        if not self.shop:
            print("Shop is empty!")
            return
        print("Shop: " + ", ".join(f"{m.name}({m.attack}/{m.health})" for m in self.shop))
