"""Watchdog objects."""
from dataclasses import dataclass

@dataclass
class WatchDog:
    """Base class for watchdog."""
    watchdog_last_minute: int
    staff_rolling_daily: int
    watchdog_total: int
    watchdog_rolling_daily: int
    staff_total: int
