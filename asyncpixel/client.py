"""A Python HypixelAPI wrapper."""

import datetime as dt
from typing import Dict, List, Optional, Any

import aiohttp

from .exceptions.exceptions import ApiNoSuccess, InvalidApiKey, RateLimitError
from .models.auctions import Auction, AuctionItem
from .models.bazaar import (
    Bazaar,
    BazaarBuySummary,
    BazaarItem,
    BazaarQuickStatus,
    BazaarSellSummary,
)
from .models.booster import Booster, Boosters
from .models.friends import Friend
from .models.games import Game
from .models.guild import Guild
from .models.key import Key
from .models.news import News
from .models.player import Player
from .models.status import Status
from .models.watchdog import WatchDog

BASE_URL = "https://api.hypixel.net/"


class Client:
    """Client class for hypixel wrapper."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """Initialise client object.

        Args:
            api_key (Optional[str], optional): hypixel api key. Defaults to None.
            session (Optional[aiohttp.ClientSession], optional): provide an aiohttp session. Defaults to None.
        """

        self.api_key = api_key

        if session:
            self.session = session
        else:
            self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Used for safe client cleanup and stuff."""
        await self.session.close()

    async def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Base function to get raw data from hypixel.

        Args:
            path (str):
                path that you wish to request from
            params (Dict, optional):
                parameters to pass into request defaults to empty dictionary

        Raises:
            RateLimitError: error if ratelimit has been reached
            InvalidApiKey: error if api key is invalid
            ApiNoSuccess: error if api throughs an error

        Returns:
            dict: returns a dictionary of the json response
        """
        if params is None:
            params = {}

        params["key"] = self.api_key

        response = await self.session.get(f"{BASE_URL}{path}", params=params)

        if response.status == 429:
            raise RateLimitError("Hypixel")

        data: Dict[str, Any] = await response.json()
        if "cause" in data:
            if data["cause"] == "Invalid API key":
                raise InvalidApiKey()

        if not data["success"]:
            raise ApiNoSuccess()

        return data

    async def get_watchdog_stats(self) -> WatchDog:
        """Get current watchdog stats.

        Returns:
            WatchDog: WatchDog stats object
        """
        data = await self.get("watchdogstats")

        return WatchDog(
            watchdog_last_minute=data["watchdog_lastMinute"],
            staff_rolling_daily=data["staff_rollingDaily"],
            watchdog_total=data["watchdog_total"],
            watchdog_rolling_daily=data["watchdog_rollingDaily"],
            staff_total=data["staff_total"],
        )

    async def get_key_data(self, key: Optional[str] = None) -> Key:
        """Get information about an api key.

        Args:
            key (str, optional): api key. Defaults token provided in class.

        Returns:
            Key: Key object
        """
        if not key:
            key = self.api_key

        data = await self.get("key")

        return Key(
            key=data["record"]["key"],
            owner=data["record"]["owner"],
            limit=data["record"]["limit"],
            queries_in_past_min=data["record"]["queriesInPastMin"],
            total_queries=data["record"]["totalQueries"],
        )

    async def get_boosters(self) -> Boosters:
        """Get the current online boosters.

        Returns:
            Boosters: object containing boosters
        """
        data = await self.get("boosters")
        boosterlist = []

        for boost in data["boosters"]:
            boosterlist.append(
                Booster(
                    _id=boost["_id"],
                    purchaser_uuid=boost["purchaserUuid"],
                    amount=boost["amount"],
                    original_length=boost["originalLength"],
                    length=boost["length"],
                    game_type=boost["gameType"],
                    date_activated=dt.datetime.fromtimestamp(
                        boost["dateActivated"] / 1000
                    ),
                    stacked=boost["stacked"] if "stacked" in boost else False,
                )
            )
        return Boosters(
            booster_statedecrementing=data["boosterState"]["decrementing"],
            boosters=boosterlist,
        )

    async def get_player_count(self) -> int:
        """Get the current amount of players online.

        Returns:
            int: number of online players
        """
        data = await self.get("playerCount")

        return int(data["playerCount"])

    async def get_news(self) -> List[News]:
        """Get current skyblock news.

        Returns:
            List[News]: List of news objects
        """
        data = await self.get("skyblock/news")
        news_list = []
        for item in data["items"]:
            news_list.append(
                News(
                    material=item["item"]["material"],
                    link=item["link"],
                    text=item["text"],
                    title=item["title"],
                )
            )

        return news_list

    async def get_player_status(self, uuid: str) -> Status:
        """Get current online status about a player.

        Args:
            uuid (str): uuid of player

        Returns:
            Status: Status object of player
        """
        uuid = uuid.replace("-", "")
        data = await self.get("status", params={"uuid": uuid})
        if data["session"]["online"]:
            return Status(
                online=True,
                game_type=data["session"]["gameType"],
                _mode=data["session"]["mode"],
                _map=data["session"],
            )
        return Status(online=False)

    async def get_player_friends(self, uuid: str) -> List[Friend]:
        """Get a list of a players friends.

        Args:
            uuid (str): the uuid of the player you wish to get friends from

        Returns:
            List[Friend]: returns a list of friend elements
        """
        uuid = uuid.replace("-", "")
        params = {"uuid": uuid}
        data = await self.get("friends", params=params)

        friend_list = []
        for friend in data["records"]:
            friend_list.append(
                Friend(
                    _id=friend["_id"],
                    uuid_sender=friend["uuidSender"],
                    uuid_receiver=friend["uuidReceiver"],
                    started=dt.datetime.fromtimestamp(friend["started"] / 1000),
                )
            )

        return friend_list

    async def get_bazaar(self) -> Bazaar:
        """Get info of the items in the bazaar.

        Returns:
            Bazaar: object for bazzar
        """
        data = await self.get("skyblock/bazaar")

        bazaar_items = []

        for name in data["products"]:
            elements = data["products"][name]
            sell_summary = []
            buy_summary = []
            for sell in elements["sell_summary"]:
                sell_summary.append(
                    BazaarSellSummary(
                        amount=sell["amount"],
                        price_per_unit=sell["pricePerUnit"],
                        orders=sell["orders"],
                    )
                )
            for buy in elements["buy_summary"]:
                buy_summary.append(
                    BazaarBuySummary(
                        amount=buy["amount"],
                        price_per_unit=buy["pricePerUnit"],
                        orders=buy["orders"],
                    )
                )
            quick = elements["quick_status"]
            bazaar_quick_status = BazaarQuickStatus(
                product_id=quick["productId"],
                sell_price=quick["sellPrice"],
                sell_volume=quick["sellVolume"],
                sell_moving_week=quick["sellMovingWeek"],
                sell_orders=quick["sellOrders"],
                buy_price=quick["buyPrice"],
                buy_volume=quick["buyVolume"],
                buy_moving_week=quick["buyMovingWeek"],
                buy_orders=quick["buyOrders"],
            )
            bazaar_items.append(
                BazaarItem(
                    name=name,
                    product_id=elements["product_id"],
                    sell_summary=sell_summary,
                    buy_summary=buy_summary,
                    quick_status=bazaar_quick_status,
                )
            )

        return Bazaar(
            last_updated=dt.datetime.fromtimestamp(1590854517479 / 1000),
            bazaar_items=bazaar_items,
        )

    async def auctions(self, page: Optional[int] = 0) -> Auction:
        """Get the auctions available.

        Args:
            page (int, optional): Page of auction list you want. Defaults to 0.

        Returns:
            Auction: Auction object.
        """
        params = {"page": page}
        data = await self.get("skyblock/auctions", params=params)
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                AuctionItem(
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=dt.datetime.fromtimestamp(auc["start"] / 1000),
                    end=dt.datetime.fromtimestamp(auc["end"] / 1000),
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                    _id=auc["_id"],
                )
            )
        return Auction(
            page=data["page"],
            total_pages=data["totalPages"],
            total_auctions=data["totalAuctions"],
            last_updated=dt.datetime.fromtimestamp(data["lastUpdated"] / 1000),
            auctions=auction_list,
        )

    async def get_recent_games(self, uuid: str) -> List[Game]:
        """Get recent games of a player.

        Args:
            uuid (str): uuid of player

        Returns:
            List[Game]: list of recent games
        """
        uuid = uuid.replace("-", "")
        params = {"uuid": uuid}
        data = await self.get("recentGames", params=params)

        games_list = []
        for game in data["games"]:
            if "ended" in game:
                games_list.append(
                    Game(
                        date=dt.datetime.fromtimestamp(game["date"] / 1000),
                        game_type=game["gameType"],
                        mode=game["Mode"],
                        _map=game["map"],
                        ended=dt.datetime.fromtimestamp(game["ended"] / 1000),
                    )
                )
            else:
                games_list.append(
                    Game(
                        date=dt.datetime.fromtimestamp(game["date"] / 1000),
                        game_type=game["gameType"],
                        mode=game["Mode"],
                        _map=game["map"],
                    )
                )

        return games_list

    async def get_player(self, uuid: str) -> Player:
        """Get information about a player from their uuid.

        Args:
            uuid (str): uuid of player

        Returns:
            Player: player object
        """
        uuid = uuid.replace("-", "")
        params = {"uuid": uuid}
        data = await self.get("player", params=params)

        return Player(
            _id=data["player"]["_id"],
            uuid=data["player"]["uuid"],
            first_login=dt.datetime.fromtimestamp(data["player"]["firstLogin"] / 1000),
            playername=data["player"]["playername"],
            last_login=dt.datetime.fromtimestamp(data["player"]["lastLogin"] / 1000),
            displayname=data["player"]["displayname"],
            known_aliases=data["player"]["knownAliases"],
            known_aliases_lower=data["player"]["knownAliasesLower"],
            achievements_one_time=data["player"]["achievementsOneTime"],
            mc_version_rp=data["player"]["mcVersionRp"],
            network_exp=data["player"]["networkExp"],
            karma=data["player"]["karma"],
            spec_always_flying=data["player"]["spec_always_flying"],
            last_adsense_generate_time=data["player"]["lastAdsenseGenerateTime"],
            last_claimed_reward=data["player"]["lastClaimedReward"],
            total_rewards=data["player"]["totalRewards"],
            total_daily_rewards=data["player"]["totalDailyRewards"],
            reward_streak=data["player"]["rewardStreak"],
            reward_score=data["player"]["rewardScore"],
            reward_high_score=data["player"]["rewardHighScore"],
            last_logout=dt.datetime.fromtimestamp(data["player"]["lastLogout"] / 1000),
            friend_requests_uuid=data["player"]["friendRequestsUuid"],
            network_update_book=data["player"]["network_update_book"],
            achievement_tracking=data["player"]["achievementTracking"],
            achievement_points=data["player"]["achievementPoints"],
            current_gadget=data["player"]["currentGadget"],
            channel=data["player"]["channel"],
            most_recent_game_type=data["player"]["mostRecentGameType"],
            level=self.calc_player_level(data["player"]["networkExp"]),
        )

    @staticmethod
    def calc_player_level(xp: int) -> int:
        """Calculate player level from xp.

        Args:
            xp (int): amount of xp a player has

        Returns:
            int: current level of player
        """
        return int(1 + (-8750.0 + (8750 ** 2 + 5000 * xp) ** 0.5) / 2500)

    async def find_guild_by_name(self, name: str) -> str:
        """Find guild id by name.

        Args:
            name (str): name of guild

        Returns:
            str: id of guild
        """
        params = {"byName": name}
        data = await self.get("findGuild", params=params)
        return str(data["guild"])

    async def find_guild_by_uuid(self, uuid: str) -> str:
        """Find guild by uuid.

        Args:
            uuid (str): uuid of guild

        Returns:
            str: id of guild
        """
        uuid = uuid.replace("-", "")
        params = {"byUuid": uuid}
        data = await self.get("findGuild", params=params)
        return str(data["guild"])

    async def get_guild_by_name(self, guild_name: str) -> Guild:
        """Get guild by name.

        Args:
            guild_name (str): name of guild

        Returns:
            Guild: guild object
        """
        params = {"name": guild_name}
        data = await self.get("guild", params=params)
        guild_object = self.create_guild_object(data)
        return guild_object

    async def get_guild_by_id(self, guild_id: int) -> Guild:
        """Get guild by id.

        Args:
            guild_id (int): id of guild

        Returns:
            Guild: guild object
        """
        params = {"id": guild_id}
        data = await self.get("guild", params=params)
        guild_object = self.create_guild_object(data)
        return guild_object

    async def get_guild_by_player(self, player_uuid: str) -> Guild:
        """Get guild by player.

        Args:
            player_uuid (str): uuid of a player in the guild

        Returns:
            Guild: guild object
        """
        player_uuid = player_uuid.replace("-", "")
        params = {"player": player_uuid}
        data = await self.get("guild", params=params)
        guild_object = self.create_guild_object(data)
        return guild_object

    @staticmethod
    def create_guild_object(data: Dict[str, Any]) -> Guild:
        """Create guild object from json.

        Args:
            data (dict): json

        Returns:
            Guild: guild object
        """
        guild = data["guild"]
        return Guild(
            _id=guild["_id"],
            created=dt.datetime.fromtimestamp(guild["created"] / 1000),
            name=guild["name"],
            name_lower=guild["name_lower"],
            description=guild["description"],
            tag=guild["tag"],
            tag_color=guild["tagColor"],
            exp=guild["exp"],
            members=guild["members"],
            achievements=guild["achievements"],
            ranks=guild["ranks"],
            joinable=guild["joinable"],
            legacy_ranking=guild["legacyRanking"],
            publicly_listed=guild["publiclyListed"],
            hide_gm_tag=guild["hideGmTag"],
            preferred_games=guild["preferredGames"],
            chat_mute=guild["chatMute"],
            guild_exp_by_game_type=guild["guildExpByGameType"],
            banner=guild["banner"],
        )

    async def get_auction_from_uuid(self, uuid: str) -> List[AuctionItem]:
        """Get auction from uuid.

        Args:
            uuid (str): minecraft uuid

        Returns:
            List[Auction_item]: list of auctions
        """
        params = {"uuid": uuid}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    async def get_auction_from_player(self, player: str) -> List[AuctionItem]:
        """Get auction data from player.

        Args:
            player (str): player

        Returns:
            List[Auction_item]: list of auction items
        """
        params = {"player": player}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    async def get_auction_from_profile(self, profile_id: str) -> List[AuctionItem]:
        """Get auction data from profile.

        Args:
            profile_id (str): profile id

        Returns:
            List[Auction_item]: list of auction items
        """
        params = {"profile": profile_id}
        data = await self.get("skyblock/auction", params=params)
        auction_items = self.create_auction_object(data)
        return auction_items

    @staticmethod
    def create_auction_object(data: Dict[str, Any]) -> List[AuctionItem]:
        """Create auction object.

        Args:
            data (Dict): json input

        Returns:
            List[Auction_item]: auction object list
        """
        auction_list = []
        for auc in data["auctions"]:
            auction_list.append(
                AuctionItem(
                    _id=auc["_id"],
                    uuid=auc["uuid"],
                    auctioneer=auc["auctioneer"],
                    profile_id=auc["profile_id"],
                    coop=auc["coop"],
                    start=dt.datetime.fromtimestamp(auc["start"] / 1000),
                    end=dt.datetime.fromtimestamp(auc["end"] / 1000),
                    item_name=auc["item_name"],
                    item_lore=auc["item_lore"],
                    extra=auc["extra"],
                    category=auc["category"],
                    tier=auc["tier"],
                    starting_bid=auc["starting_bid"],
                    item_bytes=auc["item_bytes"],
                    claimed=auc["claimed"],
                    claimed_bidders=auc["claimed_bidders"],
                    highest_bid_amount=auc["highest_bid_amount"],
                    bids=auc["bids"],
                )
            )
        return auction_list

    # NOT FULLY IMPLEMENTED

    # async def get_profile(self, profile: str) -> Dict:
    #     """Get profile info of a skyblock player.

    #     Args:
    #         profile (str): profile id of player ca be gotten from
    #                         running get_profiles

    #     Returns:
    #         Dict: json response
    #     """
    #     params = {"profile": profile}
    #     data = await self.get("skyblock/profile", params=params)
    #     return data["profile"]

    # async def get_profiles(self, uuid: str) -> Dict:
    #     """Get info on a profile.

    #     Args:
    #         uuid (str): uuid of player

    #     Returns:
    #         Dict: json response
    #     """
    #     uuid = uuid.replace("-", "")
    #     params = {"uuid": uuid}
    #     data = await self.get("skyblock/profiles", params=params)
    #     return data["profiles"]

    # async def get_game_count(self) -> Dict:# type: ignore
    #     """Get the current game count.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("gameCounts")
    #     return data["games"]

    # async def get_leaderboard(self) -> Dict:# type: ignore
    #     """Get the current leaderboards.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("leaderboards")
    #     return data["leaderboards"]

    # async def get_resources_achievements(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/achievements")
    #     return data["achievements"]

    # async def get_resources_challenges(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/challenges")
    #     return data["challenges"]

    # async def get_resources_quests(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/quests")
    #     return data["quests"]

    # async def get_resources_guilds_achievements(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/guilds/achievements")
    #     return data["guilds/achievements"]

    # async def get_resources_guilds_permissions(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/guilds/permissions")
    #     return data["guilds/permissions"]

    # async def get_resources_skyblock_collections(self) -> Dict:# type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/skyblock/collections")
    #     return data["skyblock/collections"]

    # async def get_resources_skyblock_skills(self) -> Dict: # type: ignore
    #     """Get the current resources. Does not require api key.

    #     Returns:
    #         dict: raw json response
    #     """
    #     data = await self.get("resources/skyblock/skills")
    #     return data["skyblock/skills"]
