"""Status data class."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Status:
    """Status data object."""

    online: bool
    game_type: Optional[str] = None
    _mode: Optional[str] = None
    _map: Optional[str] = None
