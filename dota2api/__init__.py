#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dota 2 API wrapper and parser in Python"""

__author__ = "Joshua Duffy, Evaldo Bratti"
__date__ = "29/10/2014"
__version__ = "1.3.3"
__licence__ = "GPL"

import json
import collections

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import os
import requests
from requests_futures.sessions import FuturesSession
import asyncio
from aiohttp import ClientSession

from .src import urls, exceptions, response, parse


class Initialise(object):
    """When calling this you need to provide the ``api_key``
    You can also specify a ``language``

    :param api_key: (str) string with the ``api key``
    :param logging: (bool, optional) set this to True for logging output
    """

    def __init__(self, api_key=None, executor=None, logging=None, language=None):
        if api_key:
            self.api_key = api_key
        elif 'D2_API_KEY' in os.environ:
            self.api_key = os.environ['D2_API_KEY']
        else:
            raise exceptions.APIAuthenticationError()

        if not executor:
            # self.executor = requests.get
            self.executor = FuturesSession().get
        else:
            self.executor = executor

        if not language:
            self.language = 'en_us'
        else:
            self.language = language

        if logging:
            self.logger = _setup_logger()
        else:
            self.logger = None

        self.__format = "json"

    def get_friends_list(self, steamid, **kwargs):
        steamid = convert_to_64_bit(steamid)
        if steamid not in kwargs:
            kwargs['steamid'] = steamid

        kwargs['relationship'] = 'friend'

        return self.__dota_request(url=urls.GET_FRIENDS_LIST, **kwargs)

    def get_match_history(self, account_id=None, **kwargs):
        """Returns a dictionary containing a list of the most recent Dota matches

        :param account_id: (int, optional)
        :param hero_id: (int, optional)
        :param game_mode: (int, optional) see ``ref/modes.json``
        :param skill: (int, optional) see ``ref/skill.json``
        :param min_players: (int, optional) only return matches with minimum
            amount of players
        :param league_id: (int, optional) for ids use ``get_league_listing()``
        :param start_at_match_id: (int, optional) start at matches equal to or
            older than this match id
        :param matches_requested: (int, optional) defaults to ``100``
        :param tournament_games_only: (str, optional) limit results to
            tournament matches only
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'account_id' not in kwargs:
            kwargs['account_id'] = account_id
        return self.__dota_request(url=urls.GET_MATCH_HISTORY, **kwargs)

    def get_match_history_by_seq_num(self, start_at_match_seq_num=None, **kwargs):
        """Returns a dictionary containing a list of Dota matches in the order they were recorded

        :param start_at_match_seq_num: (int, optional) start at matches equal to or
            older than this match id
        :param matches_requested: (int, optional) defaults to ``100``
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'start_at_match_seq_num' not in kwargs:
            kwargs['start_at_match_seq_num'] = start_at_match_seq_num
        return self.__dota_request(url=urls.GET_MATCH_HISTORY_BY_SEQ_NUM, **kwargs)

    def get_match_details(self, match_id=None, **kwargs):
        """Returns a dictionary containing the details for a Dota 2 match

        :param match_id: (int, optional)
        :return: dictionary of matches, see :doc:`responses </responses>`
        """
        if 'match_id' not in kwargs:
            kwargs['match_id'] = match_id
        return self.__dota_request(url=urls.GET_MATCH_DETAILS, **kwargs)

    def get_open_match_data(self, match_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_MATCHES, match_id, **kwargs)

    def get_open_player(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER, account_id, **kwargs)

    def get_open_player_win_loose(self, account_id, **kwargs):
        """
        :param account_id: (int, required)
        :param limit: (int, optional) Number of matches to limit to
        :param offset: (int, optional) Number of matches to offset start by
        :param win: (int, optional)	Whether the player won
        :param patch: (int, optional) Patch ID
        :param game_mode: (int, optional) Game Mode ID
        :param lobby_type: (int, optional) Lobby type ID
        :param region: (int, optional) Region ID
        :param date: (int, optional) Days previous
        :param lane_role: (int, optional) Lane Role ID
        :param hero_id: (int, optional)	Hero ID
        :param is_radiant: (int, optional) Whether the player was radiant
        :param included_account_id: (int, optional)	Account IDs in the match (array)
        :param excluded_account_id: (int, optional)	Account IDs not in the match (array)
        :param with_hero_id: (int, optional) Hero IDs on the player's team (array)
        :param against_hero_id: (int, optional)	Hero IDs against the player's team (array)
        :param significant: (int, optional)	Whether the match was significant for aggregation purposes. Defaults to 1 (true), set this to 0 to return data for non-standard modes/matches.
        :param having: (int, optional) The minimum number of games played, for filtering hero stats
        :param sort: (int, optional) The field to return matches sorted by in descending order
        :param project: (int, optional)	Fields to project (array)
        :return: Dictionary of amount of lost and won games
        """
        return self.__open_dota_request(urls.OPEN_PLAYER_WL, account_id, **kwargs)

    def get_open_player_recent_matches(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_RECENT_MATCHES, account_id, **kwargs)

    def get_open_player_matches(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_MATCHES, account_id, **kwargs)

    def get_open_player_heroes(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_HEROES, account_id, **kwargs)

    def get_open_player_peers(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_PEERS, account_id, **kwargs)

    def get_open_player_pros(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_PROS, account_id, **kwargs)

    def get_open_player_totals(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_TOTALS, account_id, **kwargs)

    def get_open_player_counts(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_COUNTS, account_id, **kwargs)

    def get_open_player_histograms(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_HISTOGRAMS, account_id, **kwargs)

    def get_open_player_wardmap(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_WARDMAP, account_id, **kwargs)

    def get_open_player_wordcloud(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_WORDCLOUD, account_id, **kwargs)

    def get_open_player_ratings(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_RATINGS, account_id, **kwargs)

    def get_open_player_rankings(self, account_id, **kwargs):
        return self.__open_dota_request(urls.OPEN_PLAYER_RANKINGS, account_id, **kwargs)

    def get_stratz_player(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER, value=steam_id, **kwargs)

    def get_stratz_players(self, steam_ids: list = None, **kwargs):
        if 'steamId' not in kwargs:
            kwargs['steamId'] = ','.join(map(str, steam_ids))
        return self.__stratz_dota_request(urls.STRATZ_PLAYERS, **kwargs)

    def get_stratz_player_matches(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_MATCHES, steam_id, **kwargs)

    def get_stratz_player_cards(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_CARDS, steam_id, **kwargs)

    def get_stratz_player_performance(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_PERFORMANCE, steam_id, **kwargs)

    def get_stratz_player_hero_performance(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_HERO_PERFORMANCE, steam_id, **kwargs)

    # work on it
    def get_stratz_player_single_hero_performance(self, steam_id=None, hero_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_SINGLE_HERO_PERFORMANCE, steam_id, hero_id, **kwargs)

    def get_stratz_player_behavior_chart(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_BEHAVIOR_CHART, steam_id, **kwargs)

    def get_stratz_player_season_leaderboard(self, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_SEASON_LEADERBOARD, **kwargs)

    def get_stratz_player_history(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_HISTORY, steam_id, **kwargs)

    def get_stratz_player_card_hover(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_CARD_HOVER, steam_id, **kwargs)

    def get_stratz_player_dotaplus_leaderboard(self, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_DOTAPLUS_LEADERBOARD, **kwargs)

    def get_stratz_player_pro_steam_account(self, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_PRO_STEAM_ACCOUNT, **kwargs)

    def get_stratz_player_battlepass_leaderboard(self, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_BATTLEPASS_LEADERBOARD, **kwargs)

    def get_stratz_player_played_with_pro(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_PLAYED_WITH_PRO, steam_id, **kwargs)

    def get_stratz_player_summary(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_PLAYER_SUMMARY, steam_id, **kwargs)

    def get_stratz_draft(self, steam_ids: list = None, **kwargs):
        if 'steamId' not in kwargs:
            kwargs['steamId'] = ','.join(map(str, steam_ids))
        return self.__stratz_dota_request(urls.STRATZ_DRAFT, **kwargs)

    def get_stratz_draft_hero_highlight(self, steam_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_DRAFT_HERO_HIGHLIGHT, steam_id, **kwargs)

    def get_stratz_draft_hero_weight(self, days: int = None, **kwargs):
        if 'days' not in kwargs:
            kwargs['days'] = days
        return self.__stratz_dota_request(urls.STRATZ_DRAFT_HERO_WEIGHT, **kwargs)

    def get_stratz_match(self, matchId=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_MATCH, matchId, **kwargs)

    def get_stratz_matches(self, matchId: list = None, **kwargs):
        if 'matchId' not in kwargs:
            kwargs['matchId'] = ','.join(map(str, matchId))
        return self.__stratz_dota_request(urls.STRATZ_MATCHES, **kwargs)

    def get_stratz_match_breakdown(self, match_id=None, **kwargs):
        return self.__stratz_dota_request(urls.STRATZ_MATCH_BREAKDOWN, match_id, **kwargs)





    def get_league_listing(self, **kwargs):
        """Returns a dictionary containing a list of all ticketed leagues

        :return: dictionary of ticketed leagues, see :doc:`responses </responses>`
        """
        return self.__dota_request(url=urls.GET_LEAGUE_LISTING, **kwargs)

    def get_live_league_games(self, **kwargs):
        """Returns a dictionary containing a list of ticked games in progress

        :return: dictionary of live games, see :doc:`responses </responses>`
        """
        return self.__dota_request(url=urls.GET_LIVE_LEAGUE_GAMES, **kwargs)

    def get_team_info_by_team_id(self, start_at_team_id=None, **kwargs):
        """Returns a dictionary containing a in-game teams

        :param start_at_team_id: (int, optional)
        :param teams_requested: (int, optional)
        :return: dictionary of teams, see :doc:`responses </responses>`
        """
        if 'start_at_team_id' not in kwargs:
            kwargs['start_at_team_id'] = start_at_team_id
        return self.__dota_request(url=urls.GET_TEAM_INFO_BY_TEAM_ID, **kwargs)

    def get_player_summaries(self, steamids=None, **kwargs):
        """Returns a dictionary containing a player summaries

        :param steamids: (list) list of ``32-bit`` or ``64-bit`` steam ids, notice
                                that api will convert if ``32-bit`` are given
        :return: dictionary of player summaries, see :doc:`responses </responses>`
        """
        if not isinstance(steamids, collections.Iterable):
            steamids = [steamids]

        base64_ids = list(map(convert_to_64_bit, filter(lambda x: x is not None, steamids)))

        if 'steamids' not in kwargs:
            kwargs['steamids'] = base64_ids
        return self.__dota_request(url=urls.GET_PLAYER_SUMMARIES, **kwargs)

    def get_heroes(self, **kwargs):
        """Returns a dictionary of in-game heroes, used to parse ids into localised names

        :return: dictionary of heroes, see :doc:`responses </responses>`
        """
        return self.__dota_request(url=urls.GET_HEROES, **kwargs)

    def get_game_items(self, **kwargs):
        """Returns a dictionary of in-game items, used to parse ids into localised names

        :return: dictionary of items, see :doc:`responses </responses>`
        """
        return self.__dota_request(url=urls.GET_GAME_ITEMS, **kwargs)

    def get_tournament_prize_pool(self, leagueid=None, **kwargs):
        """Returns a dictionary that includes community funded tournament prize pools

        :param leagueid: (int, optional)
        :return: dictionary of prize pools, see :doc:`responses </responses>`
        """
        if 'leagueid' not in kwargs:
            kwargs['leagueid'] = leagueid
        return self.__dota_request(url=urls.GET_TOURNAMENT_PRIZE_POOL, **kwargs)

    def get_top_live_games(self, partner='', **kwargs):
        """Returns a dictionary that includes top MMR live games

        :param partner: (int, optional)
        :return: dictionary of prize pools, see :doc:`responses </responses>`
        """
        if 'partner' not in kwargs:
            kwargs['partner'] = partner
        return self.__dota_request(url=urls.GET_TOP_LIVE_GAME, **kwargs)

    def update_game_items(self):
        """
        Update the item reference data via the API
        """
        new_items = {}

        items = self.get_game_items()
        parse.parse_items_images_urls(items)

        for item in items['items']:
            new_items[item['id']] = item
            dict.pop(new_items[item['id']], 'id')
        _save_dict_to_file(new_items, "items.json")

    def update_heroes(self):
        """
        Update the hero reference data via the API
        """
        new_heroes = {}

        heroes = self.get_heroes()
        parse.parse_heroes_images(heroes)

        for hero in heroes['heroes']:
            new_heroes[hero['id']] = hero
            dict.pop(new_heroes[hero['id']], 'id')
        _save_dict_to_file(new_heroes, "heroes.json")

    def __get_open_dota_url(self, url: str, value, **kwargs):
        return self.__build_url_modern(url.format(value), urls.OPEN_DOTA_BASE_URL, **kwargs)

    def __get_stratz_dota_url(self, url: str, value, **kwargs):
        return self.__build_url_modern(url.format(value), urls.STRATZ_BASE_URL, **kwargs)

    def __get_dota_url(self, url: str, **kwargs):
        return self.__build_url(url, **kwargs)

    def __open_dota_request(self, url: str, value, **kwargs):
        exists = kwargs.pop('get_url', None)
        url = self.__get_open_dota_url(url, value, **kwargs)
        if exists:
            return url
        return self.__request_build_dict(url)

    def __stratz_dota_request(self, url: str, value='', **kwargs):
        exists = kwargs.pop('get_url', None)
        url = self.__get_stratz_dota_url(url, value, **kwargs)
        if exists:
            return url
        return self.__request_build_dict(url)

    def __dota_request(self,  url: str, **kwargs):
        exists = kwargs.pop('get_url', None)
        url = self.__get_dota_url(url, **kwargs)
        if exists:
            return url
        return self.__request_build_dict(url)

    def __build_url(self, api_call, **kwargs):
        """Builds the api query"""
        kwargs['key'] = self.api_key
        if 'language' not in kwargs:
            kwargs['language'] = self.language
        if 'format' not in kwargs:
            kwargs['format'] = self.__format
        api_query = urlencode(kwargs)

        return "{0}{1}?{2}".format(urls.BASE_URL,
                                   api_call,
                                   api_query)

    def __build_url_modern(self, api_call, base_url, **kwargs):
        api_query = urlencode(kwargs)
        if 'steamId' in kwargs:
            api_query = f"steamId={kwargs['steamId']}"
        return "{0}{1}?{2}".format(base_url,
                                   api_call,
                                   api_query)

    async def build_async_request(self, func, lst, **kwargs):
        urls = self.get_urls(func, lst, **kwargs)
        cor = asyncio.ensure_future(self.run(urls))
        while not cor.done():
            await asyncio.sleep(1)
        return cor.result()

    def get_urls(self, func, lst, **kwargs):
        kwargs['get_url'] = True
        return [func(i, **kwargs) for i in lst]

    async def fetch(self, url, session):
        async with session.get(url) as resp:
            # return await resp.read()
            return await resp.read()

    async def run(self, urls):
        tasks = []

        async with ClientSession() as session:
            for url in urls:
                task = asyncio.ensure_future(self.fetch(url, session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

        results = []
        for resp in responses:
            results.append(self.__request_build_dict_from_async(resp))

        return results

    def __request_build_dict_from_async(self, req):
        # if not self.__check_http_err(req.status_code):
        #     print('converting to json')
        return response.build(req)

    def __request_build_dict(self, url):
        req = self.executor(url).result()
        if self.logger:
            self.logger.info('URL: {0}'.format(url))
        if not self.__check_http_err(req.status_code):
            print('converting to json')
            return response.build(req, url)

    def __check_http_err(self, status_code):
        """Raises an exception if we get a http error"""
        if status_code == 403:
            raise exceptions.APIAuthenticationError(self.api_key)
        elif status_code == 503:
            raise exceptions.APITimeoutError()
        else:
            return False


def convert_to_64_bit(number):
    min64b = 76561197960265728
    if number < min64b:
        return number + min64b
    return number


def convert_to32_bit(number):
    number = int(number)
    min64b = 76561197960265728
    if number > min64b:
        return number - min64b
    return number


def _setup_logger():
    import logging
    logging.basicConfig(level=logging.NOTSET)  # Will log all
    return logging.getLogger(__name__)


def _save_dict_to_file(json_dict, file_name):
    out_file = open(parse.load_json_file(file_name), "w")
    json.dump(json_dict, out_file, indent=4)
    out_file.close()
