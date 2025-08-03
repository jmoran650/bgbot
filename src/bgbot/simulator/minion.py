"""minion.py
Defines `Tribe` enum and `Minion` data class for the Hearthstone Battlegrounds simulator.
"""
from __future__ import annotations
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from .events import Effect, EventBus, Event, EventType

if TYPE_CHECKING:
    from .player import Player


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
    DRAGON = "dragon"
    NEUTRAL = "neutral"
    ALL = "all"

@dataclass
class Minion():
    """A basic Battlegrounds minion with combat-relevant stats and metadata."""
    name: str
    attack: int
    health: int
    tier: int
    owner: Player
    tribes: List[Tribe]
    keywords: list[str] = field(default_factory=lambda: [])
    effects: list[str] = field(default_factory=lambda: [])
    _effects_instances: List[Effect] = field(default_factory=list, repr=False)

    def __post_init__(self) -> None:
        if not self.tribes:
            raise ValueError("Minion must have at least one tribe.")
        self._initialize_effects()

    def _initialize_effects(self):
        """Based on the 'effects' list, create instances of the effect classes."""
        for effect_name in self.effects:
            if effect_name == 'eternal_knight':
                self._effects_instances.append(EternalKnightEffect(self))

    def attach_to_game(self, event_bus: EventBus):
        """Attaches all of this minion's effects to the event bus."""
        for effect in self._effects_instances:
            effect.attach(event_bus)

    def detach_from_game(self):
        """Detaches all of this minion's effects from the event bus."""
        for effect in self._effects_instances:
            effect.detach()

    def buff(self, attack_increment: int, health_increment: int) -> None:
        """Increase this minion's stats by the supplied amounts."""
        self.attack += attack_increment
        self.health += health_increment

    def take_damage(self, damage: int):
        """Reduces the minion's health by the damage amount."""
        self.health -= damage
        logging.info(f"- {self.name} takes {damage} damage, health is now {self.health}.")

    @property
    def is_alive(self) -> bool:
        """Checks if the minion's health is above zero."""
        return self.health > 0

    # Optional: nicer debug display.
    def __repr__(self) -> str:  # pragma: no cover
        tribe_names = "/".join(t.value for t in self.tribes)
        return f"<Minion {self.attack}/{self.health} [{tribe_names}]>"


class EternalKnightEffect(Effect):
    """Handles the stat-scaling logic for Eternal Knight."""

    def attach(self, event_bus: EventBus):
        """On attach, apply buffs for any knights that have already died."""
        super().attach(event_bus)
        
        # Get the current death count from the player's state
        initial_bonus = self.minion.owner.permanent_buffs.get('eternal_knight_deaths', 0)

        if initial_bonus > 0:
            self.minion.buff(initial_bonus, initial_bonus)
            logging.info(f"✨ New Eternal Knight on {self.minion.owner.name}'s board gets +{initial_bonus}/+{initial_bonus} bonus.")

    def _register_listeners(self):
        if self.event_bus:
            self.event_bus.subscribe(EventType.MINION_DIES, self._on_minion_death)

    def _unregister_listeners(self):
        if self.event_bus:
            self.event_bus.unsubscribe(EventType.MINION_DIES, self._on_minion_death)

    def _on_minion_death(self, event: Event):
        """When a friendly Eternal Knight dies, update the player's counter and buff all other friendly knights."""
        if (event.player is not self.minion.owner or 
            'eternal_knight' not in event.source.effects or
            event.source is self.minion):
            return

        if not hasattr(event, '_ek_death_counted'):
            event._ek_death_counted = True
            
            # 1. Increment the counter on the Player object
            current_count = self.minion.owner.permanent_buffs.get('eternal_knight_deaths', 0)
            self.minion.owner.permanent_buffs['eternal_knight_deaths'] = current_count + 1
            logging.info(f"PLAYER STATE (via Effect): {self.minion.owner.name}'s EK death count is now {current_count + 1}.")

        # 2. Buff this specific knight instance
        self.minion.buff(1, 1)
        logging.info(f"BUFF: {self.minion.name} on {self.minion.owner.name}'s board is now {self.minion.attack}/{self.minion.health}")
