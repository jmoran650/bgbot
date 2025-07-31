from .board import Board
# from .minion import Minion
from .player import Player
from .pool import Pool
# from .minion import Tribe

class Tavern:
    def __init__(self, pool: Pool):
        self.shop = []
        self.hand = []
        self.player = Player("Player", "Default Hero")
        self.tavern_board = Board(self.player.name, [])
        self.pool = pool
        self.tavern_tier = 1
        self.is_frozen = False

    def roll(self, count: int = 3) -> None:
        """
        Roll for new minions in the shop.
        
        Args:
            count: Number of minions to roll for (default 3)
        """
        # Return current shop minions to pool before rolling
        self._return_shop_to_pool()
        
        # Get new minions from pool
        new_shop = self.pool.roll(self.tavern_tier, count)
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
        self.tavern_tier += 1
        return True


