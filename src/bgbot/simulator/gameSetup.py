



#START A NEW GAME, INSTANTIATE GAME()?

#DETERMINE WHAT TRIBES ARE IN RANDOMLY
import random
from .minion import Tribe

def pick_random_tribes():
    """
    Randomly select 5 unique tribes from the Tribe enum.
    Returns a list of 5 Tribe members.
    """
    all_tribes = list(Tribe)
    return random.sample(all_tribes, 5)


#ALL PLAYERS SELECT HEROES (HEROES ARE TODO)


#SHOP PHASE THEN COMBAT PHASE UNTIL ONE PLAYER LEFT
