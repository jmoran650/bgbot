import logging
from simulator.player import Player
from simulator.minion import Minion, Tribe
from simulator.pool import Pool
from simulator.events import EventBus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_eternal_knight(player: Player) -> Minion:
    """Factory function to create an Eternal Knight for a specific player."""
    return Minion(
        name="Eternal Knight",
        attack=4,
        health=1,
        tier=3,
        owner=player,
        tribes=[Tribe.UNDEAD],
        effects=['eternal_knight']
    )

def run_test_scenario():
    """
    Tests the Eternal Knight "wherever this is" buff mechanic.
    
    Requirements:
    1. When a friendly Eternal Knight dies, all other friendly Eternal Knights
       (on board, in hand, in the tavern) get +1/+1 permanently.
    2. The buff is retained. When a new Eternal Knight is played, it should
       receive a buff equal to the number of friendly Knights that have
       died this game.
    """
    print("--- Running Eternal Knight Test Scenario ---")

    # Setup: One player, empty pool for simplicity
    pool = Pool(active_tribes={Tribe.UNDEAD})
    event_bus = EventBus()
    player = Player(name="TestPlayer", hero="TestHero", pool=pool, event_bus=event_bus)

    # 1. Create three Eternal Knights and add them to the board
    print("\nStep 1: Player summons three Eternal Knights.")
    knight1 = create_eternal_knight(player)
    knight2 = create_eternal_knight(player)
    knight3 = create_eternal_knight(player)

    player.board.add_minion(knight1)
    player.board.add_minion(knight2)
    player.board.add_minion(knight3)

    print(f"Board state: {player.board}")
    assert knight1.attack == 4 and knight2.attack == 4 and knight3.attack == 4

    # 2. Simulate the death of the first knight
    print("\nStep 2: First Eternal Knight dies.")
    knight1.take_damage(10) # Overkill
    player.board.remove_dead_minions()

    print(f"Board state: {player.board}")
    
    # Verification: The other two knights should be buffed
    assert knight2.attack == 5 and knight2.health == 2
    assert knight3.attack == 5 and knight3.health == 2
    print("✅ Verification PASSED: Remaining knights were buffed.")

    # 3. Simulate the death of the second knight
    print("\nStep 3: Second Eternal Knight dies.")
    knight2.take_damage(10)
    player.board.remove_dead_minions()

    print(f"Board state: {player.board}")
    
    # Verification: The last knight should be buffed again
    assert knight3.attack == 6 and knight3.health == 3
    print("✅ Verification PASSED: Last knight was buffed again.")

    # 4. Player gets a new Eternal Knight
    print("\nStep 4: Player summons a new Eternal Knight.")
    knight4 = create_eternal_knight(player)
    player.board.add_minion(knight4)

    print(f"Board state: {player.board}")

    # Verification: The new knight should receive the total accumulated buff
    # Two knights have died, so it should get +2/+2 upon being played.
    assert knight4.attack == 6 and knight4.health == 3
    print("✅ Verification PASSED: New knight received the full 'wherever this is' buff.")

    # 5. Simulate the death of the third knight
    print("\nStep 5: Third Eternal Knight dies.")
    knight3.take_damage(10)
    player.board.remove_dead_minions()

    print(f"Board state: {player.board}")

    # Verification: The fourth knight should be buffed
    assert knight4.attack == 7 and knight4.health == 4
    print("✅ Verification PASSED: Fourth knight was buffed by the third's death.")

    print("\n--- Test Scenario Completed Successfully! ---")

if __name__ == "__main__":
    run_test_scenario()