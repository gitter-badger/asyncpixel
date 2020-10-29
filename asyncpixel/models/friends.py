"""Data object for player friends."""
import datetime
from dataclasses import dataclass


@dataclass
class Friend:
    """Friend object."""

    _id: str
    uuid_sender: str
    uuid_receiver: str
    started: datetime.datetime
