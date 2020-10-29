"""Main class for key data."""
from dataclasses import dataclass


@dataclass
class Key:
    """Main class for key data."""

    key: str
    owner: str
    limit: int
    queries_in_past_min: int
    total_queries: int
