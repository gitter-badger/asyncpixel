"""Status data class."""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Status:
    """Status data object."""
    online: bool
    game_type: Optional[str]
    _mode: Optional[str]
    _map: Optional[str]
