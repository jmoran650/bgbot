"""game.py
Main game logic for Hearthstone Battlegrounds simulator, updated to the new
architecture in which:

    • Game owns a shared Pool and a list of Player objects.
    • Each Player constructs its own Board and Tavern.
    • Board lives only on Player; Tavern only manages the shop.
"""
from __future__ import annotations

import random
from typing import List

from .minion import Tribe
from .pool import Pool
from .player import Player
from .combat import Combat


def pick_random_tribes() -> List[Tribe]:
    """Randomly select 5 unique tribes from the Tribe enum."""
    all_tribes = list(Tribe)
    return random.sample(all_tribes, 5)


class Game:
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

        # Intro printout -----------------------------------------------------
        print("=== BATTLEGROUNDS GAME STARTED ===")
        print(f"Players: {num_players}")
        print(f"Active tribes: {[t.value for t in self.tribes]}")
        print()

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
        print("🎮 Starting Hearthstone Battlegrounds simulation...")

        while len(self.alive_players) > 1:
            print(f"\n{'=' * 50}")
            print(f"🔄 TURN {self.turn}")
            print(f"{'=' * 50}")

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
                print(f"\n🏆 GAME OVER! {winner.name} ({winner.hero}) WINS!")
                break

        print(f"\nGame completed after {self.turn} turns.")

    # -------------------------------------------------------------------- #
    # SHOP PHASE
    # -------------------------------------------------------------------- #
    def shop_phase(self) -> None:
        """Handle the shopping phase for all living players."""
        print(f"\n🛒 SHOP PHASE - Turn {self.turn}")
        print("-" * 30)

        for player in self.alive_players:
            print(f"\n{player.name}'s turn:")
            self.simulate_player_turn(player)

        print("\n✅ Shop phase complete")

    def simulate_player_turn(self, player: Player) -> None:
        """Very light AI for a single player's turn."""
        board = player.board


        print(
            f"  💰 Gold: {player.gold} | "
            f"❤️  Health: {player.health} | "
            f"🏪 Tier: {player.tavern.tier}"
        )

        # Refill gold for the turn (simple rule: turn+2 up to 10)
        player.gold = min(10, self.turn + 2)

        actions_taken = 0
        max_actions = 3  # prevent infinite loops

        while player.gold > 0 and actions_taken < max_actions:
            action = self.choose_action(player)

            if action == "roll" and player.gold >= 1:
                print(f"    🎲 {player.name} rolls the shop")
                player.tavern.roll()
                player.gold -= 1
                self.display_shop(tavern)

            elif action == "buy" and player.gold >= 3 and tavern.shop:
                # Buy a random minion if board space allows
                if board.minion_count < board.capacity:
                    idx = random.randint(0, len(tavern.shop) - 1)
                    minion = tavern.shop.pop(idx)
                    print(
                        f"    💰 {player.name} buys "
                        f"{minion.name} ({minion.attack}/{minion.health})"
                    )
                    board.add_minion(minion)
                    player.gold -= 3
                else:
                    print(f"    ❌ {player.name}'s board is full, can't buy")
                    break

            elif action == "upgrade" and player.gold >= tavern.tier:
                print(
                    f"    ⬆️  {player.name} upgrades tavern "
                    f"to tier {tavern.tier + 1}"
                )
                player.gold -= tavern.tier
                tavern.upgrade()

            elif action == "freeze" and player.gold >= 1:
                print(f"    🧊 {player.name} freezes the shop")
                tavern.freeze()
                player.gold -= 1
                break  # typically end turn after freezing

            else:
                break  # no affordable actions

            actions_taken += 1

        # End-of-turn board summary
        print(f"    🏟️  Final board: {board.minion_count} minions")
        if board.minions:
            summary = ", ".join(
                f"{m.name}({m.attack}/{m.health})" for m in board.minions
            )
            print(f"      {summary}")

    # -------------------------------------------------------------------- #
    # AI decision helper
    # -------------------------------------------------------------------- #
    def choose_action(self, player: Player) -> str:
        """
        Decide what the (very dumb) AI should do this action.
        Possible returns: "roll", "buy", "upgrade", "freeze".
        """
        tavern = player.tavern
        board = player.board

        # Early game: prioritise buying cheap bodies
        if self.turn <= 3:
            if not tavern.shop:
                return "roll"
            if board.minion_count < 4:
                return "buy"
            return "upgrade"

        # Mid game: balance upgrades and board building
        if self.turn <= 6:
            if tavern.tier < 3 and player.gold >= tavern.tier:
                return "upgrade"
            if not tavern.shop:
                return "roll"
            return "buy"

        # Late game
        if tavern.tier < 5 and player.gold >= tavern.tier:
            return "upgrade"
        return random.choice(["roll", "buy"])



    # -------------------------------------------------------------------- #
    # COMBAT PHASE
    # -------------------------------------------------------------------- #
    def combat_phase(self) -> None:
        """Run combat for paired players."""
        print(f"\n⚔️  COMBAT PHASE - Turn {self.turn}")
        print("-" * 30)

        alive = self.alive_players
        if len(alive) < 2:
            print("Not enough players for combat!")
            return

        random.shuffle(alive)

        # Pair off players
        for i in range(0, len(alive) - 1, 2):
            p1 = alive[i]
            p2 = alive[i + 1]
            print(f"\n🥊 {p1.name} vs {p2.name}")

            combat = Combat(p1.board, p2.board)
            combat.resolve_combat()

        # Odd player gets a bye
        if len(alive) % 2 == 1:
            odd_man = alive[-1]
            print(f"\n😴 {odd_man.name} had no opponent this round")

        print("\n⚔️  Combat phase complete")


# ------------------------------------------------------------------------ #
# Quick manual test
# ------------------------------------------------------------------------ #
if __name__ == "__main__":
    Game(num_players=4).run_game()