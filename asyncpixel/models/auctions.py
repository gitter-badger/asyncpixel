"""Auction related objects."""
import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Bids:
    """Bid."""

    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: datetime.datetime


@dataclass
class AuctionItem:
    """auction item class."""

    uuid: str
    auctioneer: str
    profile_id: str
    coop: List[str]
    start: datetime.datetime
    end: datetime.datetime
    item_name: str
    item_lore: str
    extra: str
    category: str
    tier: str
    starting_bid: int
    item_bytes: str
    claimed: bool
    claimed_bidders: List[str]
    highest_bid_amount: int
    bids: List[Bids]
    _id: str


@dataclass
class Auction:
    """Main auction object."""

    page: str
    total_pages: str
    total_auctions: str
    last_updated: datetime.datetime
    auctions: List[AuctionItem]
