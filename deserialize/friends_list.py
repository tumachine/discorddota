from enum import Enum
from typing import List
from dota2api import convert_to32_bit


class Friend:
    def __init__(self, dictionary: dict) -> None:
        self.steamid = convert_to32_bit(dictionary['steamid'])
        self.relationship = dictionary['relationship']
        self.friend_since = dictionary['friend_since']


class Friendslist:
    def __init__(self, steamid, dictionary) -> None:
        self.steamid = steamid
        friendslist = dictionary.get('friendslist')
        if not friendslist:
            print('Profile is private')
            self.friends = []
        else:
            self.friends = [Friend(friend) for friend in friendslist['friends']]

    def has_friend(self, steamid):
        for friend in self.friends:
            if friend.steamid == steamid:
                return True
        return False
