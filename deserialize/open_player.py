class MmrEstimate:
    def __init__(self, dictionary: dict) -> None:
        self.estimate = dictionary['estimate']


class Profile:
    def __init__(self, dictionary: dict) -> None:
        self.account_id = dictionary['account_id']
        self.personaname = dictionary['personaname']
        self.name = dictionary['name']
        self.cheese = dictionary['cheese']
        self.steamid = dictionary['steamid']
        self.avatar = dictionary['avatar']
        self.avatarmedium = dictionary['avatarmedium']
        self.avatarfull = dictionary['avatarfull']
        self.profileurl = dictionary['profileurl']
        self.last_login = dictionary['last_login']
        self.loccountrycode = dictionary['loccountrycode']
        self.is_contributor = dictionary['is_contributor']


class Player:
    def __init__(self, dictionary: dict) -> None:
        self.tracked_until = dictionary['tracked_until']
        self.profile = Profile(dictionary['profile'])
        self.solo_competitive_rank = dictionary['solo_competitive_rank']
        self.mmr_estimate = MmrEstimate(dictionary['mmr_estimate'])
        self.rank_tier = dictionary['rank_tier']
        self.leaderboard_rank = dictionary['leaderboard_rank']
        self.competitive_rank = dictionary['competitive_rank']
