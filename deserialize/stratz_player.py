from typing import List, Any
from utils.util import replace_dict_null
import datetime


class Name:
    name: str
    last_seen_date_time: int

    def __init__(self, dictionary: dict) -> None:
        self.name = dictionary['name']
        self.last_seen_date_time = dictionary['lastSeenDateTime']


class Rank:
    season_id: int
    rank: int

    def __init__(self, dictionary: dict) -> None:
        self.season_id = dictionary['seasonRankId']
        self.rank = dictionary['rank']


class Team:
    team_name: str
    date: int

    def __init__(self, dictionary: dict) -> None:
        self.team_name = dictionary['teamName']
        self.date = dictionary['date']


class StratzPlayer:
    def __init__(self, dictionary: dict) -> None:
        dictionary = replace_dict_null(
            ['name', 'ranks', 'leaderBoardRank'],
            ['Unknown', [], 'Not on'],
            dictionary
        )
        self.dict = dictionary
        self.name = dictionary.get('name')
        self.date = dictionary.get('date')
        self.steam_id = dictionary.get('steamId')
        self.profile_url = dictionary.get('profileUrl')
        self.avatar = dictionary.get('avatar')
        self.avatar_medium = dictionary.get('avatarMedium')
        self.avatar_full = dictionary.get('avatarFull')
        self.is_verified = dictionary.get('isVerified')
        self.last_region_id = dictionary.get('lastRegionId')
        self.is_dota_plus_subscriber = dictionary.get('isDotaPlusSubscriber')
        # self.battle_pass_level = dictionary['battlePassLevel']
        if dictionary.get('ranks') is None:
            self.ranks = []
        else:
            self.ranks = [Rank(rank) for rank in dictionary.get('ranks')]
        self.language_code = dictionary.get('languageCode')
        self.is_anonymous = dictionary.get('isAnonymous')
        self.first_match_date = dictionary.get('firstMatchDate')
        self.match_count = dictionary.get('matchCount')
        self.win_count = dictionary.get('winCount')
        if dictionary.get('names') is None:
            self.names = []
        else:
            self.names = [Name(name) for name in dictionary.get('names')]

        if self.win_count is None or self.match_count is None:
            self.winrate = 0
        else:
            self.winrate = round(self.win_count / (self.match_count / 100), 2)
        self.leaderboard_rank = dictionary.get('leaderBoardRank')

    def get_current_and_previous_rank(self):
        previous_rank = 1
        rank = 1
        for stratz_rank in self.ranks:
            if stratz_rank.season_id == 2:
                previous_rank = stratz_rank.rank
            elif stratz_rank.season_id == 3:
                rank = stratz_rank.rank
        return rank, previous_rank

    def get_formatted_time(self, format_time='%Y-%m'):
        return datetime.datetime.utcfromtimestamp(self.first_match_date).strftime(format_time)
