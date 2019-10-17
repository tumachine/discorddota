from deserialize.friends_list import Friendslist
from index import api
from typing import List
from random import randint


def check_if_any_contains(first_set: set, second_set: set):
    for i in first_set:
        if i in second_set:
            return True
    return False


async def get_parties(users: List[int]):
    fr = await api.build_async_request(api.get_friends_list, users)
    # friends = [Friendslist(friend['steamid'], friend) for friend in fr]
    friends = []
    for count, friend in enumerate(fr):
        friends.append(Friendslist(users[count], friend))
    friend_groups = []

    for i in range(len(friends)):
        friend_groups.append({friends[i].steamid})
        for y in range(len(friends)):
            if i == y:
                continue
            if friends[i].has_friend(friends[y].steamid):
                friend_groups[i].add(friends[y].steamid)

    combined = []
    for i in range(len(friend_groups)):
        combined.append(friend_groups[i])
        for y in range(len(friend_groups)):
            if i == y:
                continue
            if check_if_any_contains(combined[-1], friend_groups[y]):
                combined[-1].update(friend_groups[y])
                friend_groups[y] = {}

    party_list = []
    for party in combined:
        if len(party) > 0:
            party_list.append(list(party))

    return party_list


def get_teams(players_per_team, team_amt, players):
    if len(players) % players_per_team != 0:
        raise AttributeError("There should be no remainder")

    teams: List[List] = []
    for team_num in range(team_amt):
        teams.append([])
        for player in range(players_per_team):
            teams[team_num].append(int(players[(team_num * players_per_team) + player]))

    return teams


def generate_random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def generate_random_palette_for_parties(players_per_team):
    return [generate_random_color() for player in range(players_per_team)]


async def assign_players_party_color(players, players_per_team, team_amt):
    colors = generate_random_palette_for_parties(players_per_team)

    teams = get_teams(players_per_team, team_amt, players)
    # parties = [get_parties(team) for team in teams]
    parties = []
    for team in teams:
        party = await get_parties(team)
        parties.append(party)

    players_colors = []
    for count, player in enumerate(players):
        color = (0, 0, 0)
        team_num = count // players_per_team
        for c, party in enumerate(parties[team_num]):
            if int(player) in party:
                color = colors[c]

        players_colors.append(color)

    return players_colors
