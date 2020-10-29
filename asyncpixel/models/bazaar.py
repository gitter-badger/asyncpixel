"""Bazaar classes."""

import datetime
from typing import List
from dataclasses import dataclass


@dataclass
class BazaarBuySummary:
    """Bazaar buy object."""
    amount: int
    price_per_unit: int
    orders: int


@dataclass
class BazaarSellSummary:
    """Bazaar sell object."""
    amount: int
    price_per_unit: int
    orders: int


@dataclass
class BazaarQuickStatus:
    """Bazaar quick status."""
    product_id: str
    sell_price: float
    sell_volume: int
    sell_moving_week: int
    sell_orders: int
    buy_price: float
    buy_volume: int
    buy_moving_week: int
    buy_orders: int


@dataclass
class BazaarItem:
    """Bazaar item."""
    name: str
    product_id: str
    sell_summary: List[BazaarBuySummary]
    buy_summary: List[BazaarSellSummary]
    quick_status: BazaarQuickStatus


@dataclass
class Bazaar:
    """Bazaar object."""
    last_updated: datetime.datetime
    bazaar_items: List[BazaarItem]
