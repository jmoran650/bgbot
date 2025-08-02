from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .minion import Minion

MAX_MINIONS = 7

class Board:
    """Represents the board of minions for a player."""

    MAX_MINIONS: int = 7

    def __init__(self, player_name: str, minions: list[Minion] ):
        """Initializes the Board with an empty list of minions."""
        self.player_name = player_name
        self.minions = minions
        

    def add_minion(self, minion: Minion):
        """Adds a minion to the board if there is space.

        Args:
            minion: The Minion object to add.

        Raises:
            ValueError: If the board is already full.
        """
        if len(self.minions) < self.MAX_MINIONS:
            self.minions.append(minion)
        else:
            raise ValueError("Board is full")

    def remove_minion(self, minion: Minion):
        """Removes a specific minion from the board.

        Args:
            minion: The Minion object to remove.
        """
        if minion in self.minions:
            self.minions.remove(minion)

    def get_minions(self) -> list[Minion]:
        """Returns the list of minions on the board."""
        return self.minions
    
    def remove_dead_minions(self):
        """Filters out any minions that have died during an attack."""
        initial_count = self.minion_count
        self.minions = [minion for minion in self.minions if minion.is_alive]
        if self.minion_count < initial_count:
            print(f"    - Dead minions removed from {self.player_name}'s board.")


    @property
    def minion_count(self) -> int:
        """Returns the number of minions currently on the board."""
        return len(self.minions)

    def __repr__(self) -> str:
        """Provides a string representation of the board for debugging."""
        if not self.minions:
            return "<Board: []>"
        minion_reprs = ", ".join(repr(m) for m in self.minions)
        return f"<Board: [{minion_reprs}]>"
