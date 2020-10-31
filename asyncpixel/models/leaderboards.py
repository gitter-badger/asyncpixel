"""Game Count related objects."""
from dataclasses import dataclass
from typing import List
from typing import Tuple

@dataclass
class Leaderboards:
    """Game count game."""
    path: int
    prefix: str
    title: str
    location: Tuple[int, int, int]
    count: int
    leaders: List[str]
