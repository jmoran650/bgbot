# pylint: skip-file 
# pyright: reportMissingImports=false, reportUnknownMemberType=false
from __future__ import annotations
import random
import logging
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
        version just picks a random alive minion.
        """
        valid_targets = board.alive_minions

        return random.choice(valid_targets)
    
    def resolve_combat(self) -> str:
        """
        Executes the combat loop using deques for a more robust attack sequence.
        """
        attackers1 = deque(self.board1.minions)
        attackers2 = deque(self.board2.minions)

        first_attacker = attackers1 if "board1" in self.order else attackers2

        while attackers1 and attackers2:
            
            if first_attacker is attackers1:
                # Assign the unused variable to '_'
                attacking_queue, _ = attackers1, attackers2
                defending_board = self.board2
            else:
                # Assign the unused variable to '_'
                attacking_queue, _ = attackers2, attackers1
                defending_board = self.board1
            
            if not defending_board.alive_minions: break
            
            attacker = attacking_queue.popleft()
            target = self._find_target(defending_board)

            logging.info(f"\n--> {attacker.name} attacks {target.name}!")
            target.take_damage(attacker.attack)
            attacker.take_damage(target.attack)

            if attacker.is_alive:
                attacking_queue.append(attacker)

            self.board1.remove_dead_minions()
            self.board2.remove_dead_minions()
            attackers1 = deque([m for m in attackers1 if m.is_alive])
            attackers2 = deque([m for m in attackers2 if m.is_alive])
            
            first_attacker = attackers2 if first_attacker is attackers1 else attackers1

        # --- Determine Winner ---
        logging.info("\n" + "="*30 + "\nCombat has ended.")
        if attackers1:
            return f"{self.board1.owner.name} wins!"
        if attackers2:
            return f"{self.board2.owner.name} wins!"
        return "It's a Tie!"

