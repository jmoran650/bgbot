from __future__ import annotations
from enum import Enum
from typing import Dict, List, Callable, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
import logging

if TYPE_CHECKING:
    from .minion import Minion
    from .board import Board
    from .player import Player


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



@dataclass
class Event:
    """Base event class containing event data"""
    type: EventType
    source: Optional[Minion] = None  # The minion triggering the event
    target: Optional[Minion] = None  # The minion being affected
    board: Optional[Board] = None    # The board where event occurs
    player: Optional[Player] = None  # The player involved
    data: Dict[str, Any] = field(default_factory=dict)  # Additional event data


class EventBus:
    """Central event dispatcher for the game"""
    
    def __init__(self):
        # Maps event types to lists of callback functions
        self._listeners: Dict[EventType, List[Callable[[Event], None]]] = {}
        
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """Subscribe a callback to an event type"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        self._listeners[event_type].append(callback)
        logging.debug(f"Subscribed to {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """Remove a callback from an event type"""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            logging.debug(f"Unsubscribed from {event_type.value}")
    
    def emit(self, event: Event):
        """Dispatch an event to all registered listeners"""
        logging.info(f"🔔 Event: {event.type.value}")
        
        if event.type in self._listeners:
            # Copy the list to avoid issues if listeners modify subscriptions
            listeners = self._listeners[event.type].copy()
            for callback in listeners:
                try:
                    callback(event)
                except Exception as e:
                    logging.error(f"Error in event handler: {e}")


# Base Effect class for minion abilities
from abc import ABC, abstractmethod


class Effect(ABC):
    """Base class for all minion effects"""
    
    def __init__(self, minion: Minion):
        self.minion = minion
        self.event_bus: Optional[EventBus] = None
        
    def attach(self, event_bus: EventBus):
        """Called when effect is attached to the event system"""
        self.event_bus = event_bus
        self._register_listeners()
        
    def detach(self):
        """Called when effect is removed or minion dies"""
        if self.event_bus:
            self._unregister_listeners()
            self.event_bus = None
        
    @abstractmethod
    def _register_listeners(self):
        """Subscribe to relevant events"""
        pass
        
    @abstractmethod
    def _unregister_listeners(self):
        """Unsubscribe from events"""
        pass