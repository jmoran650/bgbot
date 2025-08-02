"""game.py
Main game logic for Hearthstone Battlegrounds simulator, updated to the new
architecture in which:

    • Game owns a shared Pool and a list of Player objects.
    • Each Player constructs its own Board and Tavern.
    • Board lives only on Player; Tavern only manages the shop.
"""
from __future__ import annotations
import random
import logging
import os
from datetime import datetime

from typing import List

from .minion import Tribe
from .pool import Pool
from .player import Player
from .combat import Combat


def setup_logging() -> str:
    """
    Configures file logging into a 'logs' directory with a unique filename.
    Format: [color]-[animal]-[timestamp].log
    Returns the path to the created log file.
    """
    os.makedirs("logs", exist_ok=True)

    # 1. Define lists for both colors and animals.
    colors = [
        "red", "blue", "green", "yellow", "purple", "orange", "golden",
        "iron", "shadow", "crystal", "azure", "crimson", "jade"
    ]
    animals = [
        "whelp", "hydra", "macaw", "raptor", "hyena", "kodo",
        "wolf", "bear", "lion", "tiger", "serpent", "elemental"
    ]
    
    # 2. Choose one from each list.
    random_color = random.choice(colors)
    random_animal = random.choice(animals)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    log_filename = os.path.join(
        "logs", 
        f"{random_color}-{random_animal}-{timestamp}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        filename=log_filename,
        filemode="w"
    )
    return log_filename

def pick_random_tribes() -> List[Tribe]:
    """Randomly select 5 unique tribes from the Tribe enum."""
    all_tribes = list(Tribe)
    return random.sample(all_tribes, 5)


class Game:
    """
    Manages the overall state and flow of a Hearthstone Battlegrounds game,
    including players, turns, and combat phases.
    """
    def __init__(self, num_players: int = 4) -> None:
        """
        Start a new Battlegrounds game.

        Args:
            num_players: Number of players in the lobby (max 8 in BG).
        """
        # Global setup -------------------------------------------------------
        self.tribes = pick_random_tribes()
        self.pool: Pool = Pool(set(self.tribes))

        hero_names = [
            "Reno", "Flurgl", "Patches", "Millhouse",
            "Galewing", "Lich King", "Rafaam", "Toki",
        ]

        # Create the players (each makes its own Tavern & Board) ------------
        self.players: List[Player] = []
        for idx in range(num_players):
            name = f"Player {idx + 1}"
            hero = hero_names[idx % len(hero_names)]
            self.players.append(Player(name, hero, self.pool))

        # Game-state trackers ------------------------------------------------
        self.turn: int = 1
        self.phase: str = "SHOP"  # alternates SHOP <-> COMBAT

        # Intro logging.infoout -----------------------------------------------------
        logging.info("=== BATTLEGROUNDS GAME STARTED ===")
        logging.info(f"Players: {num_players}")
        logging.info(f"Active tribes: {[t.value for t in self.tribes]}")
        logging.info("")

    # -------------------------------------------------------------------- #
    # Properties
    # -------------------------------------------------------------------- #
    @property
    def alive_players(self) -> List[Player]:
        """All players whose health is above zero."""
        return [p for p in self.players if p.alive]

    # -------------------------------------------------------------------- #
    # Main loop
    # -------------------------------------------------------------------- #
    def run_game(self) -> None:
        """Run the full simulation until there is only one player left."""
        logging.info("🎮 Starting Hearthstone Battlegrounds simulation...")

        while len(self.alive_players) > 1:
            logging.info(f"\n{'=' * 50}")
            logging.info(f"🔄 TURN {self.turn}")
            logging.info(f"{'=' * 50}")

            if self.phase == "SHOP":
                self.shop_phase()
                self.phase = "COMBAT"
            else:
                self.combat_phase()
                self.phase = "SHOP"
                self.turn += 1

            # Victory check
            if len(self.alive_players) == 1:
                winner = self.alive_players[0]
                logging.info(f"\n🏆 GAME OVER! {winner.name} ({winner.hero}) WINS!")
                break

        logging.info(f"\nGame completed after {self.turn} turns.")

    # -------------------------------------------------------------------- #
    # SHOP PHASE
    # -------------------------------------------------------------------- #
    def shop_phase(self) -> None:
        """Handle the shopping phase for all living players."""
        logging.info(f"\n🛒 SHOP PHASE - Turn {self.turn}")
        logging.info("-" * 30)

        for player in self.alive_players:
            logging.info(f"\n{player.name}'s turn:")
            self.simulate_player_turn(player)

        logging.info("\n✅ Shop phase complete")

    def simulate_player_turn(self, player: Player) -> None:
        """Very light AI for a single player's turn."""
        board = player.board

        tavern = player.tavern
        tavern.start_of_turn_refresh()

        player.gold = min(10, self.turn + 2)

        actions_taken = 0
        max_actions = 3


        logging.info(
            f"  💰 Gold: {player.gold} | "
            f"❤️  Health: {player.health} | "
            f"🏪 Tier: {player.tavern.tier}"
        )

        # Refill gold for the turn (simple rule: turn+2 up to 10)



        while player.gold > 0 and actions_taken < max_actions:
            action = self.choose_action(player)

            if action == "roll" and player.gold >= 1:
                logging.info(f"    🎲 {player.name} rolls the shop")
                player.tavern.reroll_shop()
                player.gold -= 1
                player.tavern.display_shop()

            elif action == "buy" and player.gold >= 3 and tavern.shop:
                # Buy a random minion if board space allows
                if board.minion_count < board.capacity:
                    idx = random.randint(0, len(tavern.shop) - 1)
                    minion = tavern.shop.pop(idx)
                    logging.info(
                        f"    💰 {player.name} buys "
                        f"{minion.name} ({minion.attack}/{minion.health})"
                    )
                    board.add_minion(minion)
                    player.gold -= 3
                else:
                    logging.info(f"    ❌ {player.name}'s board is full, can't buy")
                    break

            elif action == "upgrade" and player.gold >= tavern.tier:
                logging.info(
                    f"    ⬆️  {player.name} upgrades tavern "
                    f"to tier {tavern.tier + 1}"
                )
                player.gold -= tavern.tier
                player.tavern.upgrade_tavern()

            elif action == "freeze" and player.gold >= 1:
                logging.info(f"    🧊 {player.name} freezes the shop")
                tavern.freeze()
                player.gold -= 1
                break  # typically end turn after freezing

            else:
                break  # no affordable actions

            actions_taken += 1

        # End-of-turn board summary
        logging.info(f"    🏟️  Final board: {board.minion_count} minions")
        if board.minions:
            summary = ", ".join(
                f"{m.name}({m.attack}/{m.health})" for m in board.minions
            )
            logging.info(f"      {summary}")

    # -------------------------------------------------------------------- #
    # AI decision helper
    # -------------------------------------------------------------------- #
    def choose_action(self, player: Player) -> str:
        """
        A simple, random AI that only chooses from valid actions.
        """
        tavern = player.tavern
        board = player.board
        gold = player.gold

        possible_actions: List[str] = []

        # Check if buying is possible
        if gold >= 3 and tavern.shop and not board.is_full:
            possible_actions.append("buy")

        # Check if upgrading is possible
        if gold >= tavern.upgrade_cost and tavern.tier < 6:
            possible_actions.append("upgrade")

        # Check if rolling is possible
        if gold >= 1:
            possible_actions.append("roll")


        # If there are any possible actions, choose one at random
        if possible_actions:
            return random.choice(possible_actions)

        # If no actions are possible, end the turn
        return "end_turn"


    # -------------------------------------------------------------------- #
    # COMBAT PHASE
    # -------------------------------------------------------------------- #
    def combat_phase(self) -> None:
        """Run combat for paired players."""
        logging.info(f"\n⚔️  COMBAT PHASE - Turn {self.turn}")
        logging.info("-" * 30)

        alive = self.alive_players
        if len(alive) < 2:
            logging.info("Not enough players for combat!")
            return

        random.shuffle(alive)

        # Pair off players
        for i in range(0, len(alive) - 1, 2):
            p1 = alive[i]
            p2 = alive[i + 1]
            logging.info(f"\n🥊 {p1.name} vs {p2.name}")

            # Create deep copies of the boards to use in combat
            combat_board1 = p1.board.clone_for_combat()
            combat_board2 = p2.board.clone_for_combat()

            # Pass the copies, not the original boards
            combat = Combat(combat_board1, combat_board2)
            winner = combat.resolve_combat()

            # Calculate damage based on the state of the copied boards after combat
            if p1.name in winner:
                damage_dealt = p1.tavern.tier + sum(m.tier for m in combat.board1.minions) # Get tier from blueprint
                p2.take_damage(damage_dealt)
            elif p2.name in winner:
                damage_dealt = p2.tavern.tier + sum(m.tier for m in combat.board2.minions) # Get tier from blueprint
                p1.take_damage(damage_dealt)
            
        # Odd player gets a bye
        if len(alive) % 2 == 1:
            odd_man = alive[-1]
            logging.info(f"\n😴 {odd_man.name} had no opponent this round")

        logging.info("\n Combat phase complete")


# ------------------------------------------------------------------------ #
# Quick manual test
# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    log_file_path = setup_logging()
    Game(num_players=8).run_game()