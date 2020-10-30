"""Profile objects."""
import datetime
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Members:
    """Member."""
    last_save: datetime.datetime
    inv_armor
    first_join: datetime.datetime
    first_join_hub: int
    stats
    objectives
    tutorial: List
    quests
    coin_purse: int
    last_death: datetime.datetime
    crafted_generators: List
    visited_zones: List
    fairy_souls_collected: int
    fairy_souls: int
    death_count: int
    slayer_bosses
    pets: List


@dataclass
class Profile:
    """Profile."""
    profile_id: str
    cute_name: str
    members: Dict[str, Members]