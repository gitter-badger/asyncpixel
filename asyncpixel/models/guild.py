"""Guild objects."""

import datetime
from typing import Dict, List, Union, Optional
from dataclasses import dataclass


@dataclass
class Banner:
    """Banner for the guild."""

    Base: int
    Patterns: List[Dict[str, Union[int, str]]]


@dataclass
class Members:
    """Members in a guild."""

    uuid: str
    rank: str
    joined: datetime.datetime
    exp_history: Dict[str, int]
    quest_participation: int
    muted_till: Optional[datetime.datetime]


@dataclass
class Rank:
    """Rank."""

    name: str
    default: bool
    created: int
    priority: int
    tag: str


@dataclass
class Guild:
    """Guild object."""

    _id: str
    created: datetime.datetime
    name: str
    name_lower: str
    description: str
    tag: str
    tag_color: str
    exp: int
    members: List[Members]
    achievements: Dict[str, int]
    ranks: List[Rank]
    joinable: bool
    legacy_ranking: int
    publicly_listed: bool
    hide_gm_tag: bool
    preferred_games: List[str]
    chat_mute: datetime.datetime
    guild_exp_by_game_type: Dict[str, str]
    banner: Banner
