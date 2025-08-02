# pylint: skip-file 
# pyright: reportMissingImports=false, reportUnknownMemberType=false
from __future__ import annotations
import random
from collections import deque
from .board import Board
from .minion import Minion #, Tribe



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
    

    def _find_target(self, board: Board) -> Minion:
        """
        Finds a valid target on the board.
        A real implementation would handle Taunt here. This simplified
        version just picks a random minion.
        """
        return random.choice(board.minions)
    
    def resolve_combat(self) -> str:
        """
        Executes the combat loop using deques for a more robust attack sequence.
        """
        # 1. Create attacker queues from the initial boards
        attackers1 = deque(self.board1.minions)
        attackers2 = deque(self.board2.minions)

        first_attacker = attackers1 if "board1" in self.order else attackers2

        while attackers1 and attackers2: # Loop while both queues have minions
            
            # Determine who is attacking and defending this turn
            if first_attacker is attackers1:
                attacking_queue, _defending_queue = attackers1, attackers2
                defending_board = self.board2
            else:
                attacking_queue, _defending_queue = attackers2, attackers1
                defending_board = self.board1
            
            # 2. Get the next attacker from the front of the queue
            attacker = attacking_queue.popleft()
            
            # Find a target (must be from the original board to find taunts, etc.)
            # This part still needs the full board state
            if not defending_board.alive_minions: break # Opponent has no one left
            target = self._find_target(defending_board)

            print(f"\n--> {attacker.name} attacks {target.name}!")
            target.take_damage(attacker.attack)
            attacker.take_damage(target.attack)

            # 3. If the attacker survived, put it at the end of its line
            if attacker.is_alive:
                attacking_queue.append(attacker)

            # 4. CRITICAL: Remove any dead minions from BOTH queues and boards
            # This is the most complex part of the deque logic
            self.board1.remove_dead_minions()
            self.board2.remove_dead_minions()
            attackers1 = deque([m for m in attackers1 if m.is_alive])
            attackers2 = deque([m for m in attackers2 if m.is_alive])
            
            # Swap turns for the next loop iteration
            first_attacker = attackers2 if first_attacker is attackers1 else attackers1

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
                print(f"\n--> {self.board1.owner.name}'s {attacker.name} attacks {target.name}!")

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
                print(f"\n--> {self.board2.owner.name}'s {attacker.name} attacks {target.name}!")

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
            return f"{self.board1.owner.name} wins!"
        if self.board2.minion_count > 0:
            return f"{self.board2.owner.name} wins!"
        return "It's a Tie!"
