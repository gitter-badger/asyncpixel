"""Player objects."""

import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class Player:
    """Player object."""

    _id: str
    uuid: str
    first_login: datetime.datetime
    playername: str
    last_login: datetime.datetime
    displayname: str
    known_aliases: List[str]
    known_aliases_lower: List[str]
    achievements_one_time: List[str]
    mc_version_rp: str
    network_exp: int
    karma: int
    spec_always_flying: bool
    last_adsense_generate_time: datetime.datetime
    last_claimed_reward: int
    total_rewards: int
    total_daily_rewards: int
    reward_streak: int
    reward_score: int
    reward_high_score: int
    last_logout: datetime.datetime
    friend_requests_uuid: List[str]
    network_update_book: str
    achievement_tracking: List[str]
    achievement_points: int
    current_gadget: str
    channel: str
    most_recent_game_type: str
    level: int
