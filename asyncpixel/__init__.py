"""Asyncpixel.

An asyncronous hypixel api wrapper
"""

try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore

from .client import Client

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
__author__ = "Leon Bowie"

__all__ = [
    "__version__",
    "__author__",
    "Client",
]
