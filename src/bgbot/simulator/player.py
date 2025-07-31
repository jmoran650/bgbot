

class Player():
    def __init__(self, name, hero):
        self.name = name
        self.hero = hero
        self.health = 30
        self.alive = True
    
    def take_damage(self, damage: int):
        self.health -= damage
        if self.health < 0:
            self.game_over()
    
    def game_over(self):
        self.alive = False