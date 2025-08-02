from enum import Enum
from typing import Dict, List, Callable, Any
from dataclasses import dataclass


class EventType(Enum):
    '''
    Contains all different kinds of events
    Jibbum please add more if you can think of others
    
    '''

    # Combat events
    COMBAT_START = "combat_start"
    MINION_ATTACKS = "minion_attacks"
    MINION_TAKES_DAMAGE = "minion_takes_damage"
    MINION_DIES = "minion_dies"
    COMBAT_END = "combat_end"
    
    # Shop events  
    MINION_PLAYED = "minion_played"
    MINION_SOLD = "minion_sold"
    TURN_START = "turn_start"
    TURN_END = "turn_end"
    
    # Minion events
    MINION_SUMMONED = "minion_summoned"
    MINION_BUFFED = "minion_buffed"



