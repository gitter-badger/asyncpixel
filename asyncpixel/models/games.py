"""Game related objects."""

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Game:
    """Game class."""

    date: datetime.datetime
    game_type: str
    mode: str
    _map: str
    ended: Optional[datetime.datetime] = None
