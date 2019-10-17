from typing import List


class Player:
    account_id: int
    player_slot: int
    hero_id: int

    def __init__(self, dictionary: dict) -> None:
        self.account_id = dictionary.get('account_id')
        self.player_slot = dictionary['player_slot']
        self.hero_id = dictionary['hero_id']


class Match:
    match_id: int
    match_seq_num: int
    start_time: int
    lobby_type: int
    radiant_team_id: int
    dire_team_id: int
    players: List[Player]

    def __init__(self, dictionary: dict) -> None:
        self.match_id = dictionary['match_id']
        self.match_seq_num = dictionary['match_seq_num']
        self.start_time = dictionary['start_time']
        self.lobby_type = dictionary['lobby_type']
        self.radiant_team_id = dictionary['radiant_team_id']
        self.dire_team_id = dictionary['dire_team_id']
        self.players = [Player(player) for player in dictionary['players']]


class MatchHistory:
    status: int
    num_results: int
    total_results: int
    results_remaining: int
    matches: List[Match]

    def __init__(self, dictionary: dict):
        self.status = dictionary['status']
        self.num_results = dictionary['num_results']
        self.total_results = dictionary['total_results']
        self.results_remaining = dictionary['results_remaining']
        self.matches = [Match(match) for match in dictionary['matches']]


