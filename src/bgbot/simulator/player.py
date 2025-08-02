from __future__ import annotations
from typing import TYPE_CHECKING

from .board import Board
from .tavern import Tavern

if TYPE_CHECKING:
    from .pool import Pool


class Player():
    """Represents a player in a Hearthstone Battlegrounds game."""

    def __init__(self, name: str, hero: str, pool: "Pool"):
        """Initializes a Player instance.

        Args:
            name: The name of the player.
            hero: The name of the hero the player is using.
            pool: The shared minion pool for the game.
        """
        self.name = name
        self.hero = hero
        self.health = 30
        self.alive = True
        self.armor = 0
        # A player creates and owns their board and tavern instance.
        self.board = Board(player_name=self.name, minions=[])
        self.tavern = Tavern(owner=self, pool=pool)
        self.gold: int = 3

    def take_damage(self, damage: int):
        """Reduces the player's health by the specified amount of damage.

        If the player's health drops to 0 or below, they are eliminated.

        Args:
            damage: The amount of damage to take.
        """
        self.health -= damage
        if self.health <= 0:
            self.game_over()

    def game_over(self):
        """Sets the player's status to not alive."""
        self.alive = False
