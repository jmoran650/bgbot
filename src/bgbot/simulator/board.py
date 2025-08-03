"""board.py
Represents the minion lineup a single player brings into combat.

Key points
----------
• A Board is created by its owning Player (`Board(owner=self)` inside
  player.py).
• Capacity is configurable but defaults to 7, matching Battlegrounds.
• All minion-management helpers live here; combat code consumes them.
"""

from __future__ import annotations
from copy import deepcopy
import logging
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:  # avoids runtime circular imports
    from .minion import Minion
    from .player import Player


class Board:
    """Container for a player's in-combat minions."""

    def __init__(self, owner: "Player") -> None:
        self.owner: Player = owner
        self.capacity: int = 7
        self.minions: List[Minion] = []  # starts empty

    def clone_for_combat(self) -> "Board":
        """
        Creates a deep copy of the board for combat simulation.
        The new board has the same owner but contains deep copies of the minions,
        ensuring that combat does not affect the player's original board state.
        """
        combat_board = Board(owner=self.owner)
        combat_board.capacity = self.capacity
        combat_board.minions = [deepcopy(m) for m in self.minions]
        return combat_board
    # Minion helpers

    def add_minion(self, minion: "Minion") -> None:
        """Add `minion` to the board, raising if the board is full."""
        if len(self.minions) >= self.capacity:
            raise ValueError("Board is full")
        minion.attach_to_game(self.owner.event_bus)
        self.minions.append(minion)

    def remove_minion(self, minion: "Minion") -> None:
        """Remove `minion` from the board if present."""
        if minion in self.minions:
            minion.detach_from_game()
            self.minions.remove(minion)

    def remove_dead_minions(self) -> None:
        """Strip out any minions whose health ≤ 0, triggering death effects."""
        dead_minions = [m for m in self.minions if not m.is_alive]
        if not dead_minions:
            return

        logging.info(f"  - Removing {len(dead_minions)} dead minion(s) from {self.owner.name}'s board.")
        
        # The Board emits the event, not the minion itself.
        for minion in dead_minions:
            if self.owner.event_bus:
                # Emit a generic event with all necessary context
                from .events import Event, EventType
                death_event = Event(
                    type=EventType.MINION_DIES,
                    source=minion,
                    player=self.owner
                )
                self.owner.event_bus.emit(death_event)
            
            # Now, detach the minion from the game
            minion.detach_from_game()

        self.minions = [m for m in self.minions if m.is_alive]
    
    # Convenience properties
    
    @property
    def minion_count(self) -> int:
        return len(self.minions)

    @property
    def is_full(self) -> bool:
        return len(self.minions) >= self.capacity

    @property
    def alive_minions(self) -> List["Minion"]:
        return [m for m in self.minions if m.is_alive]

    
    # Debugging / display
    
    def __repr__(self) -> str:
        if not self.minions:
            return f"<Board({self.owner.name}): []>"
        minion_str = ", ".join(repr(m) for m in self.minions)
        return f"<Board({self.owner.name}): [{minion_str}]>"