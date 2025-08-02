"""game.py
Main game logic for Hearthstone Battlegrounds simulator.
"""
import random
from .minion import Tribe
from .pool import Pool
from .tavern import Tavern
from .combat import Combat


def pick_random_tribes():
    """
    Randomly select 5 unique tribes from the Tribe enum.
    Returns a list of 5 Tribe members.
    """
    all_tribes = list(Tribe)
    return random.sample(all_tribes, 5)

class Game():
    
    def __init__(self, num_players: int = 4):
        
        ''' 
        Instantiate the game class to start a new battelgrounds
        games

        Args: 
            num_players: Number of players

        '''

        self.tribes = pick_random_tribes()
        self.pool = Pool(set(self.tribes))

        # Create taverns with players - each tavern owns its player
        self.taverns = []

        # we need to instantiate taverns and players for the number of players in the game
        # for our taverns all we need is to pass in the pool
        # for our players all we need is to pass in is a unique name and hero

        hero_names = ["Reno", "Flurgl", "Patches", "Millhouse", "Galewing", "Lich King", "Rafaam", "Toki"]


        for players in range(num_players):
            # instantiates taverns for however many players are in the game
            tavern = Tavern(self.pool)
            #
            tavern.player.name = f"player {players + 1}"
            tavern.player.hero = hero_names[players % len(hero_names)]
            self.taverns.append(tavern)


        self.turn = 1
        self.game_state = "SHOP"
        
        print(f"=== BATTLEGROUNDS GAME STARTED ===")
        print(f"Players: {num_players}")
        print(f"Active tribes: {[t.value for t in self.tribes]}")
        print()

    @property
    def alive_taverns(self):
        """Returns taverns with living players."""
        return [t for t in self.taverns if t.player.alive]

    def run_game(self):
        """Main game loop."""
        print("🎮 Starting Hearthstone Battlegrounds simulation...")
        
        while len(self.alive_taverns) > 1:
            print(f"\n{'='*50}")
            print(f"🔄 TURN {self.turn}")
            print(f"{'='*50}")
            
            if self.game_state == "SHOP":
                self.shop_phase()
                self.game_state = "COMBAT"
                
            elif self.game_state == "COMBAT":
                self.combat_phase()
                self.game_state = "SHOP"
                self.turn += 1
                
            # Check win condition
            if len(self.alive_taverns) == 1:
                winner = self.alive_taverns[0]
                print(f"\n🏆 GAME OVER! {winner.player.name} ({winner.player.hero}) WINS!")
                break
                
        print(f"\nGame completed after {self.turn} turns.")

    def shop_phase(self):
        """Handle the shopping phase for all players."""
        print(f"\n🛒 SHOP PHASE - Turn {self.turn}")
        print("-" * 30)
        
        for tavern in self.alive_taverns:
            print(f"\n{tavern.player.name}'s turn:")
            self.simulate_player_turn(tavern)
            
        print("\n✅ Shop phase complete")

    def simulate_player_turn(self, tavern: Tavern):
        """Simulate a player's turn with basic AI decisions.
        
        Args:
            tavern: The tavern (containing player) taking their turn
        """
        player = tavern.player
        print(f"  💰 Gold: {getattr(player, 'gold', 3)} | "
            f"❤️  Health: {player.health} | "
            f"🏪 Tier: {tavern.tavern_tier}")
        
        # Give player gold for the turn
        if not hasattr(player, 'gold'):
            player.gold = 3  # Starting gold
        else:
            player.gold += min(10, self.turn + 2)  # Cap at 10 gold
            
        # Basic AI decision making
        actions_taken = 0
        max_actions = 3  # Prevent infinite loops
        
        while player.gold > 0 and actions_taken < max_actions:
            action = self.choose_action(tavern)
            
            if action == "roll" and player.gold >= 1:
                print(f"    🎲 {player.name} rolls the shop")
                tavern.roll()
                player.gold -= 1
                self.display_shop(tavern)
                
            elif action == "buy" and player.gold >= 3 and len(tavern.shop) > 0:
                # Try to buy a random minion if board has space
                if tavern.tavern_board.minion_count < tavern.tavern_board.MAX_MINIONS:
                    minion_idx = random.randint(0, len(tavern.shop) - 1)
                    minion = tavern.shop[minion_idx]
                    print(f"    💰 {player.name} buys {minion.name} ({minion.attack}/{minion.health})")
                    
                    # Remove from shop and add to board
                    tavern.shop.pop(minion_idx)
                    tavern.tavern_board.add_minion(minion)
                    player.gold -= 3
                else:
                    print(f"    ❌ {player.name}'s board is full, can't buy")
                    break
                    
            elif action == "upgrade" and player.gold >= tavern.tavern_tier:
                print(f"    ⬆️  {player.name} upgrades tavern to tier {tavern.tavern_tier + 1}")
                player.gold -= tavern.tavern_tier
                tavern.upgrade_tavern()
                
            elif action == "freeze" and player.gold >= 1:
                print(f"    🧊 {player.name} freezes the shop")
                tavern.freeze()
                player.gold -= 1
                break  # End turn after freezing
                
            else:
                # Can't afford any actions
                break
                
            actions_taken += 1
            
        # Show final board state
        print(f"    🏟️  Final board: {tavern.tavern_board.minion_count} minions")
        if tavern.tavern_board.minions:
            minion_summary = ", ".join([f"{m.name}({m.attack}/{m.health})" 
                                    for m in tavern.tavern_board.minions])
            print(f"      {minion_summary}")

    def choose_action(self, tavern: Tavern) -> str:
        """Basic AI to choose what action to take.
        
        Args:
            tavern: The tavern making the decision
            
        Returns:
            Action string: "roll", "buy", "upgrade", "freeze", or "end"
        """
        player = tavern.player
        
        # Early game: focus on buying minions
        if self.turn <= 3:
            if len(tavern.shop) == 0:
                return "roll"
            elif tavern.tavern_board.minion_count < 4:
                return "buy"
            else:
                return "upgrade"
                
        # Mid game: balance buying and upgrading
        elif self.turn <= 6:
            if tavern.tavern_tier < 3 and player.gold >= tavern.tavern_tier:
                return "upgrade"
            elif len(tavern.shop) == 0:
                return "roll"
            else:
                return "buy"
                
        # Late game: focus on high tier minions
        else:
            if tavern.tavern_tier < 5 and player.gold >= tavern.tavern_tier:
                return "upgrade"
            else:
                return random.choice(["roll", "buy"])

    def display_shop(self, tavern: Tavern):
        """Display current shop contents."""
        if not tavern.shop:
            print("      Shop is empty!")
        else:
            shop_summary = ", ".join([f"{m.name}({m.attack}/{m.health})" 
                                    for m in tavern.shop])
            print(f"      Shop: {shop_summary}")

    def combat_phase(self):
        """Handle combat between all players."""
        print(f"\n⚔️  COMBAT PHASE - Turn {self.turn}")
        print("-" * 30)
        
        alive_taverns = self.alive_taverns
        
        if len(alive_taverns) < 2:
            print("Not enough players for combat!")
            return
            
        # Pair up players for combat
        random.shuffle(alive_taverns)
        
        for i in range(0, len(alive_taverns) - 1, 2):
            tavern1 = alive_taverns[i]
            tavern2 = alive_taverns[i + 1]
            
            print(f"\n🥊 {tavern1.player.name} vs {tavern2.player.name}")
            
            # Skip combat if either player has no minions
            if tavern1.tavern_board.minion_count == 0 and tavern2.tavern_board.minion_count == 0:
                print("   Both players have empty boards - no combat")
                continue
            elif tavern1.tavern_board.minion_count == 0:
                self.apply_damage(tavern1.player, tavern2.player, self.turn)
                continue
            elif tavern2.tavern_board.minion_count == 0:
                self.apply_damage(tavern2.player, tavern1.player, self.turn)
                continue
                
            # Run combat
            combat = Combat(tavern1.tavern_board, tavern2.tavern_board)
            result = combat.resolve_combat()
            
            # Apply damage based on result
            if "Player 1" in result:  # tavern1 wins
                self.apply_damage(tavern2.player, tavern1.player, self.turn)
            elif "Player 2" in result:  # tavern2 wins  
                self.apply_damage(tavern1.player, tavern2.player, self.turn)
            # If tie, no damage
            
        # Handle odd player out
        if len(alive_taverns) % 2 == 1:
            odd_player = alive_taverns[-1]
            print(f"\n😴 {odd_player.player.name} had no opponent this round")
            
        print("\n⚔️  Combat phase complete")

    def apply_damage(self, losing_player, winning_player, turn: int):
        """Apply damage to losing player based on winning board."""
        # Simple damage calculation: turn number + remaining minions
        base_damage = turn
        if hasattr(winning_player, 'board') and winning_player.board:
            minion_damage = len(winning_player.board.minions)
        else:
            minion_damage = 0
            
        total_damage = base_damage + minion_damage
        
        print(f"   💥 {losing_player.name} takes {total_damage} damage!")
        losing_player.take_damage(total_damage)
        
        if not losing_player.alive:
            print(f"   💀 {losing_player.name} has been eliminated!")


# Test the game
if __name__ == "__main__":
    game = Game(num_players=4)
    game.run_game()
            
