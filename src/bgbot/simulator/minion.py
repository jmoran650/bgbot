"""minion.py
Defines `Tribe` enum and `Minion` data class for the Hearthstone Battlegrounds simulator.
"""

from enum import Enum
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

class Keyword(Enum):
    """All possible minion keywords."""
    DEATHRATTLE = "deathrattle"
    DIVINE_SHIELD = "divine_shield"
    STEALTH = "stealth"
    TAUNT = "taunt"
    REBORN = "reborn"
    VENEMOUS = "venomous"
    POISONOUS = "poisonous"


class Effect(Enum):
    """All possible minion effects."""
    BATTLECRY = "battlecry"


class Minion:
    """A basic Battlegrounds minion with combat-relevant stats and metadata."""
   
    
    def __init__(self, cardName: str, tier: int, attack: int, health: int, tribes: List[Tribe], keywords: List[Keyword] = [], effects: List[str] = []):
        self.cardName = cardName
        self.tier = tier
        self.attack = attack
        self.health = health
        self.tribes = tribes
        self.keywords = keywords
        self.effects = effects

    def __post_init__(self) -> None:
        if not self.tribes:
            raise ValueError("Minion must have at least one tribe.")

    def buff(self, attack_increment: int, health_increment: int) -> None:
        """Increase this minion's stats by the supplied amounts."""
        self.attack += attack_increment
        self.health += health_increment


    def __repr__(self) -> str:
        """Developer-friendly representation showing all details."""
        tribe_names = "/".join(t.value for t in self.tribes)
        keyword_names = "/".join(k.value for k in self.keywords) if self.keywords else "none"
        effect_names = "/".join(e.value for e in self.effects) if self.effects else "none"
        
        return f"Minion(cardName='{self.cardName}', attack={self.attack}, health={self.health}, tribes=[{tribe_names}], keywords=[{keyword_names}], effects=[{effect_names}])"

    def __str__(self) -> str:
        """User-friendly representation."""
        tribe_names = "/".join(t.value for t in self.tribes)
        return f"<{self.cardName} {self.attack}/{self.health} [{tribe_names}]>"


if __name__ == "__main__":
    # Test the Minion class
    test = Minion("Alleycat", 1, 1, [Tribe.BEAST], [Keyword.DEATHRATTLE])

    # __repr__ - for developers
    print(repr(test))
    # Output: Minion(cardName='Alleycat', attack=1, health=1, tribes=[beast], keywords=[deathrattle], effects=[none])

    # __str__ - for users  
    print(str(test))
    # Output: <Alleycat 1/1 [beast]>

    # print() uses __str__ by default
    print(test)
    # Output: <Alleycat 1/1 [beast]>




