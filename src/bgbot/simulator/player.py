"""player.py
Defines the Player class for the Battlegrounds simulator.

Key points
----------
• A Player owns exactly one Board (for combat) and one Tavern (shop UI).
• Board and Tavern are instantiated inside __init__; callers provide only
  the player's name, hero, and the shared Pool object.
"""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from .board import Board
from .events import EventBus
from .tavern import Tavern

if TYPE_CHECKING:  # Avoid circular imports at runtime
    from .pool import Pool


class Player:
    """Represents a single Battlegrounds player."""

    def __init__(self, name: str, hero: str, pool: Pool, event_bus: EventBus) -> None:
        """
        Parameters
        ----------
        name : str
            The player's display name.
        hero : str
            The Battlegrounds hero they are piloting.
        pool : Pool
            The shared minion pool; needed so the Player can create a Tavern.
        """
        # Identity & stats --------------------------------------------------
        self.name: str = name
        self.hero: str = hero
        self.health: int = 30
        self.armor: int = 0
        self.alive: bool = True

        # Economy -----------------------------------------------------------
        self.gold: int = 0  # Refilled each shop phase by Game logic

        # Permanent buffs ---------------------------------------------------
        self.permanent_buffs: Dict[str, any] = {}

        # Event Bus ---------------------------------------------------------
        self.event_bus: EventBus = event_bus

        # Owned objects -----------------------------------------------------
        self.board: Board = Board(owner=self)          # combat board
        self.tavern: Tavern = Tavern(owner=self, pool=pool)  # shop interface

    # ------------------------------------------------------------------ #
    # Gameplay helpers
    # ------------------------------------------------------------------ #
    def take_damage(self, dmg: int) -> None:
        """Lose health; if ≤0, mark player as dead."""
        self.health -= dmg
        if self.health <= 0:
            self.game_over()

    def game_over(self) -> None:
        """Set alive flag to False."""
        logging.info(f"    Returning {len(self.board.minions)} minions from {self.name}'s board to the pool.")
        for minion in self.board.minions:
            self.tavern.pool.return_minion(minion.name)
        self.alive = False
        

    # Convenience properties --------------------------------------------
    @property
    def is_alive(self) -> bool:
        """return whether a player is alive or not"""
        return self.alive

    # Debugging / display -----------------------------------------------
    def __repr__(self) -> str:
        return f"<Player {self.name} ({self.hero}) {self.health} HP>"

    def print_board(self) -> None:
        """Prints the player's current board state to the console."""
        print(f"{self.name}'s board: {self.board}")
