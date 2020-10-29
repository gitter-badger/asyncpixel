"""News related objects."""
from dataclasses import dataclass


@dataclass
class News:
    """News object."""

    material: str
    link: str
    text: str
    title: str
