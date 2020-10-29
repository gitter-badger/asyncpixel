"""Data objects for boosters."""


import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class Booster:
    """Main booster class."""

    _id: str
    purchaser_uuid: str
    amount: int
    original_length: int
    length: int
    game_type: int
    date_activated: datetime.datetime
    stacked: bool


@dataclass
class Boosters:
    """Object containing boosters."""

    booster_statedecrementing: bool
    boosters: List[Booster]
