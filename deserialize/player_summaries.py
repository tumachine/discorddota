from typing import List
from utils.util import replace_dict_null


class Player:
    def __init__(self, dictionary: dict) -> None:
        dictionary = replace_dict_null(['personaname'],
                                       ['Unknown'],
                                       dictionary)
        self.dict = dictionary
        self.steamid = dictionary.get('steamid')
        self.communityvisibilitystate = dictionary.get('communityvisibilitystate')
        self.profilestate = dictionary.get('profilestate')
        self.personaname = dictionary.get('personaname')
        self.lastlogoff = dictionary.get('lastlogoff')
        self.profileurl = dictionary.get('profileurl')
        self.avatar = dictionary.get('avatar')
        self.avatarmedium = dictionary.get('avatarmedium')
        self.avatarfull = dictionary.get('avatarfull')
        self.personastate = dictionary.get('personastate')
        self.primaryclanid = dictionary.get('primaryclanid')
        self.timecreated = dictionary.get('timecreated')
        self.personastateflags = dictionary.get('personastateflags')


class PlayerSummaries:
    players: List[Player]

    def __init__(self, dictionary: dict) -> None:
        self.players = [Player(player) for player in dictionary['players']]

