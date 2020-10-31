"""Game Count related objects."""
from dataclasses import dataclass
from typing import Dict


@dataclass
class GameCountsGame:
    """Game count game."""
    players: int
    modes: Dict[str, int]

@dataclass
class GameCounts:
    """Game Count class."""

    games: Dict[str, GameCountsGame]
    player_count: int
