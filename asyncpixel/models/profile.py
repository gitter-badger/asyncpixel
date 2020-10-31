"""Profile objects."""
import datetime
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List


@dataclass
class Quests:
    """Armor."""

    status: str
    activated_at: datetime.datetime
    activated_at_sb: datetime.datetime
    completed_at: datetime.datetime
    completed_at_sb: datetime.datetime


@dataclass
class Objective:
    """Armor."""

    status: str
    progress: int
    completed_at: datetime.datetime


@dataclass
class InvArmor:
    """Armor."""

    type: int
    data: str


@dataclass
class Members:
    """Member."""

    last_save: datetime.datetime
    inv_armor: InvArmor
    first_join: datetime.datetime
    first_join_hub: int
    stats: Dict[str, int]
    objectives: Dict[str, Objective]
    tutorial: List[str]
    quests: Dict[str, Quests]
    coin_purse: int
    last_death: datetime.datetime
    crafted_generators: List[str]
    visited_zones: List[str]
    fairy_souls_collected: int
    fairy_souls: int
    death_count: int
    slayer_bosses: Dict[str, Dict[Any, Any]]
    pets: List[Any]


@dataclass
class Profile:
    """Profile."""

    profile_id: str
    cute_name: str
    members: Dict[str, Members]
