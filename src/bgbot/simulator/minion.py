"""minion.py
Defines `Tribe` enum and `Minion` data class for the Hearthstone Battlegrounds simulator.
"""
from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import List

class Tribe(Enum):
    """All possible minion tribes. Some minions may belong to two tribes at once."""
    MECH = "mech"
    MURLOC = "murloc"
    QUILBOAR = "quilboar"
    UNDEAD = "undead"
    NAGA = "naga"
    ELEMENTAL = "elemental"
    DEMON = "demon"
    PIRATE = "pirate"
    BEAST = "beast"
    NEUTRAL = "neutral"
    ALL = "all"

@dataclass
class Minion():
    """A basic Battlegrounds minion with combat-relevant stats and metadata."""
    name: str
    attack: int
    health: int
    tribes: List[Tribe]
    keywords: List[str] = []
    effects: List[str] = []

    def __post_init__(self) -> None:
        if not self.tribes:
            raise ValueError("Minion must have at least one tribe.")

    def buff(self, attack_increment: int, health_increment: int) -> None:
        """Increase this minion's stats by the supplied amounts."""
        self.attack += attack_increment
        self.health += health_increment

    def take_damage(self, damage: int):
        """Reduces the minion's health by the damage amount."""
        self.health -= damage
        print(f"    - {self.name} takes {damage} damage, health is now {self.health}.")

    @property
    def is_alive(self) -> bool:
        """Checks if the minion's health is above zero."""
        return self.health > 0

    # Optional: nicer debug display.
    def __repr__(self) -> str:  # pragma: no cover
        tribe_names = "/".join(t.value for t in self.tribes)
        return f"<Minion {self.attack}/{self.health} [{tribe_names}]>"
