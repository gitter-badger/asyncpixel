"""Status data class."""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Status:
    """Status data object."""

    online: bool
    game_type: Optional[str] = None
    _mode: Optional[str] = None
    _map: Optional[str] = None
