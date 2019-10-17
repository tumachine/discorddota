from typing import List
from datetime import datetime


class EScore:
    id: int
    score: int
    match_count: int
    win_count: int
    imp: int

    def __init__(self, dictionary: dict) -> None:
        self.id = dictionary['id']
        self.score = dictionary['score']
        self.match_count = dictionary['matchCount']
        self.win_count = dictionary['winCount']
        self.imp = dictionary.get('imp')


class StratzPlayerHeroPerformance:
    hero_id: int
    win_count: int
    kda: int
    activity: int
    duration: int
    imp: int
    award: int
    best: int
    match_count: int
    gold_per_minute: int
    experience_per_minute: int
    lane_score: List[EScore]
    role_score: List[EScore]
    last_played: datetime

    def __init__(self, dictionary: dict) -> None:
        self.hero_id = dictionary['heroId']
        self.win_count = dictionary['winCount']
        self.kda = dictionary['kda']
        self.activity = dictionary['activity']
        self.duration = dictionary['duration']
        self.imp = dictionary['imp']
        self.award = dictionary['award']
        self.best = dictionary['best']
        self.match_count = dictionary['matchCount']
        self.gold_per_minute = dictionary['goldPerMinute']
        self.experience_per_minute = dictionary['experiencePerMinute']
        self.lane_score = [EScore(lane_score) for lane_score in dictionary['laneScore']]
        self.role_score = [EScore(role_score) for role_score in dictionary['roleScore']]
        self.last_played = dictionary['lastPlayed']


class StratzPlayerHeroPerformances:
    def __init__(self, dictionary: dict) -> None:
        self.performances = [StratzPlayerHeroPerformance(hero_performance)
                             for hero_performance in dictionary['results']]

    def sort_by_best(self, get_last_amount=3):
        return sorted(self.performances, key=lambda k: k.best)[-get_last_amount:]
