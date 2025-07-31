# pylint: skip-file 
# pyright: reportMissingImports=false, reportUnknownMemberType=false
from __future__ import annotations
import random
from .board import Board
from .minion import Minion, Tribe



class Combat:

    def __init__(self, board1: Board, board2: Board):
        self.board1 = board1
        self.board2 = board2
        self.order = self._determineOrder(board1, board2)

    def _determineOrder(self, board1: Board, board2: Board):
        if (board1.minion_count > board2.minion_count):
            return "board1 goes first"
        elif (board1.minion_count < board2.minion_count):
            return "board2 goes first"
        else:  # Equal minion counts, perform a coin flip
            flip = random.choice(["heads", "tails"])
            if flip == "heads":
                return "board1 goes first"
            else:
                return "board2 goes first"
    
    # def startOfCombat(self, board1: Board, board2: Board, order: str):
    #     if order == "board1 goes first":
    #         combat.performStartOfCombat(board1)
    #         combat.performStartOfCombat(board2)
    #     elif order == "board2 goes first":
    #         combat.performStartOfCombat(board2)
    #         combat.performStartOfCombat(board1)
    
    # def performStartOfCombat(board):
    #     #something something publish START_OF_COMBAT event to event bus?

    def _find_target(self, board: Board) -> Minion:
        """
        Finds a valid target on the board.
        A real implementation would handle Taunt here. This simplified
        version just picks a random minion.
        """
        return random.choice(board.minions)
    
    def resolve_combat(self) -> str:
        """
        Executes the main combat loop until one or both boards are empty.
        This simplified loop does not handle events, deathrattles, or other
        complex mechanics. It focuses purely on the turn-based attack sequence.
        """
        # These indices track which minion is next to attack on each board.
        attacker_idx_1 = 0
        attacker_idx_2 = 0

        # Set the first attacker based on the determined order.
        current_attacker_board = self.board1 if "board1" in self.order else self.board2

        # The loop continues as long as both boards have minions.
        while self.board1.minion_count > 0 and self.board2.minion_count > 0:
            # --- Perform one attack turn ---
            if current_attacker_board == self.board1:
                attacker = self.board1.minions[attacker_idx_1]
                target = self._find_target(self.board2)
                print(f"\n--> {self.board1.player_name}'s {attacker.name} attacks {target.name}!")

                # Both minions deal damage to each other simultaneously.
                target.take_damage(attacker.attack)
                attacker.take_damage(target.attack)

                # The turn now passes to the other board.
                current_attacker_board = self.board2
                # The next time board1 attacks, it will be the next minion in line.
                attacker_idx_1 += 1

            else: # current_attacker_board == self.board2
                attacker = self.board2.minions[attacker_idx_2]
                target = self._find_target(self.board1)
                print(f"\n--> {self.board2.player_name}'s {attacker.name} attacks {target.name}!")

                target.take_damage(attacker.attack)
                attacker.take_damage(target.attack)

                current_attacker_board = self.board1
                attacker_idx_2 += 1

            # --- Cleanup Phase ---
            # After each attack, remove any dead minions from both boards.
            self.board1.remove_dead_minions()
            self.board2.remove_dead_minions()

            # If a board is now empty, the loop will terminate.
            if self.board1.minion_count == 0 or self.board2.minion_count == 0:
                break

            # If an index is now out of bounds because minions died, reset it to 0.
            # This makes the attack order wrap around.
            if attacker_idx_1 >= self.board1.minion_count:
                attacker_idx_1 = 0
            if attacker_idx_2 >= self.board2.minion_count:
                attacker_idx_2 = 0

        # --- Determine Winner ---
        print("\n" + "="*30 + "\nCombat has ended.")
        if self.board1.minion_count > 0:
            return f"{self.board1.player_name} wins!"
        if self.board2.minion_count > 0:
            return f"{self.board2.player_name} wins!"
        return "It's a Tie!"
    
if __name__ == "__main__":
    # Setup Player 1's board
    p1_board = Board("Player 1", [
        Minion("Scallywag", 2, 1, [Tribe.PIRATE]),
        Minion("Tough Tusk", 4, 3, [Tribe.QUILBOAR])
    ])

    # Setup Player 2's board
    p2_board = Board("Player 2", [
        Minion("Wrath Weaver", 1, 3, [Tribe.DEMON]),
        Minion("Micro Machine", 2, 2, [Tribe.MECH]),
        Minion("Red Whelp", 3, 2, [Tribe.DRAGON])
    ])

    # Create and run the combat
    combat_instance = Combat(p1_board, p2_board)
    winner = combat_instance.resolve_combat()
    print(f"\nRESULT: {winner}")


