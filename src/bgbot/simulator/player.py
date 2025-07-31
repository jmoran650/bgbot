

class Player():
    """Represents a player in a Hearthstone Battlegrounds game."""

    def __init__(self, name: str, hero: str):
        """Initializes a Player instance.

        Args:
            name: The name of the player.
            hero: The name of the hero the player is using.
        """
        self.name = name
        self.hero = hero
        self.health = 30
        self.alive = True
        self.armor = 0

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
