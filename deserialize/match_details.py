from enum import Enum
from typing import List, Optional
from dota2api.src.parse import get_by_id
from utils.images import get_item_picture
from utils.image_cells_manipulation import ImageCell, TextCell
from utils.text import format_unix_to_time


class PicksBan:
    is_pick: bool
    hero_id: int
    team: int
    order: int

    def __init__(self, dictionary: dict) -> None:
        self.is_pick = dictionary['is_pick']
        self.hero_id = dictionary['hero_id']
        self.team = dictionary['team']
        self.order = dictionary['order']


class AbilityUpgrade:
    ability: int
    time: int
    level: int

    def __init__(self, dictionary: dict) -> None:
        self.ability = dictionary['ability']
        self.time = dictionary['time']
        self.level = dictionary['level']


class Player:
    account_id: int
    player_slot: int
    hero_id: int
    item_0: int
    item_1: int
    item_2: int
    item_3: int
    item_4: int
    item_5: int
    backpack_0: int
    backpack_1: int
    backpack_2: int
    kills: int
    deaths: int
    assists: int
    leaver_status: int
    last_hits: int
    denies: int
    gold_per_min: int
    xp_per_min: int
    level: int
    hero_damage: int
    tower_damage: int
    hero_healing: int
    gold: int
    gold_spent: int
    scaled_hero_damage: int
    scaled_tower_damage: int
    scaled_hero_healing: int
    ability_upgrades: List[AbilityUpgrade]
    leaver_status_name: str
    leaver_status_description: str

    def __init__(self, dictionary: dict, radiant_win) -> None:
        self.won = radiant_win
        self.dict = dictionary
        self.account_id = dictionary['account_id']
        self.player_slot = dictionary['player_slot']
        self.hero_id = dictionary['hero_id']
        self.item_0 = dictionary['item_0']
        self.item_1 = dictionary['item_1']
        self.item_2 = dictionary['item_2']
        self.item_3 = dictionary['item_3']
        self.item_4 = dictionary['item_4']
        self.item_5 = dictionary['item_5']
        self.backpack_0 = dictionary['backpack_0']
        self.backpack_1 = dictionary['backpack_1']
        self.backpack_2 = dictionary['backpack_2']
        self.kills = dictionary['kills']
        self.deaths = dictionary['deaths']
        self.assists = dictionary['assists']
        self.leaver_status = dictionary['leaver_status']
        self.last_hits = dictionary['last_hits']
        self.denies = dictionary['denies']
        self.gold_per_min = dictionary['gold_per_min']
        self.xp_per_min = dictionary['xp_per_min']
        self.level = dictionary['level']
        self.hero_damage = dictionary.get('hero_damage')
        self.tower_damage = dictionary.get('tower_damage')
        self.hero_healing = dictionary.get('hero_healing')
        self.gold = dictionary.get('gold')
        self.gold_spent = dictionary.get('gold_spent')
        self.scaled_hero_damage = dictionary.get('scaled_hero_damage')
        self.scaled_tower_damage = dictionary.get('scaled_tower_damage')
        self.scaled_hero_healing = dictionary.get('scaled_hero_healing')
        self.ability_upgrades = dictionary.get('ability_upgrades')
        abil_upgr = dictionary.get('ability_upgrades')
        if abil_upgr is None:
            self.ability_upgrades = None
        else:
            self.ability_upgrades = [AbilityUpgrade(ab_up) for ab_up in abil_upgr]
        self.leaver_status_name = dictionary.get('leaver_status_name')
        self.leaver_status_description = dictionary.get('leaver_status_description')

    def get_item_ids(self):
        item_ids = []
        for item_slot in range(6):
            item_ids.append(self.dict[f'item_{item_slot}'])
        return item_ids

    def get_hero_name(self):
        return get_by_id.heroes[str(self.hero_id)]['localized_name']

    def get_item_pictures(self):
        return [get_item_picture(item_id) for item_id in self.get_item_ids()]


class MatchDetails:
    players: List[Player]
    radiant_win: bool
    duration: int
    pre_game_duration: int
    start_time: int
    match_id: int
    match_seq_num: int
    tower_status_radiant: int
    tower_status_dire: int
    barracks_status_radiant: int
    barracks_status_dire: int
    cluster: int
    first_blood_time: int
    lobby_type: int
    human_players: int
    leagueid: int
    positive_votes: int
    negative_votes: int
    game_mode: int
    flags: int
    engine: int
    radiant_score: int
    dire_score: int
    picks_bans: List[PicksBan]
    lobby_name: str
    game_mode_name: str
    cluster_name: str

    def __init__(self, dictionary: dict) -> None:
        self.radiant_win = dictionary['radiant_win']
        self.players = []
        for count, player in enumerate(dictionary['players']):
            if count < 5:
                self.players.append(Player(player, self.radiant_win))
            else:
                self.players.append(Player(player, not self.radiant_win))

        self.duration = dictionary['duration']
        self.pre_game_duration = dictionary['pre_game_duration']
        self.start_time = dictionary['start_time']
        self.match_id = dictionary['match_id']
        self.match_seq_num = dictionary['match_seq_num']
        self.tower_status_radiant = dictionary['tower_status_radiant']
        self.tower_status_dire = dictionary['tower_status_dire']
        self.barracks_status_radiant = dictionary['barracks_status_radiant']
        self.barracks_status_dire = dictionary['barracks_status_dire']
        self.cluster = dictionary['cluster']
        self.first_blood_time = dictionary['first_blood_time']
        self.lobby_type = dictionary['lobby_type']
        self.human_players = dictionary['human_players']
        self.leagueid = dictionary['leagueid']
        self.positive_votes = dictionary['positive_votes']
        self.negative_votes = dictionary['negative_votes']
        self.game_mode = dictionary['game_mode']
        self.flags = dictionary['flags']
        self.engine = dictionary['engine']
        self.radiant_score = dictionary['radiant_score']
        self.dire_score = dictionary['dire_score']

        picks_bans = dictionary.get('picks_bans')
        if picks_bans is None:
            self.picks_bans = None
        else:
            self.picks_bans = [PicksBan(pick_ban) for pick_ban in dictionary['picks_bans']]

        self.lobby_name = get_by_id.lobbies.get(str(self.lobby_type))['name']
        self.game_mode_name = get_by_id.modes.get(str(self.game_mode))['name']
        self.region = get_by_id.get_region_name_by_cluster_id(self.cluster)

        self.duration_text = f"{self.duration // 60}:{self.duration % 60}"
        self.side_won_text = 'Radiant Won' if self.radiant_win else 'Dire Won'

    def get_player_by_id(self, steam_id):
        for player in self.players:
            if player.account_id == steam_id:
                return player

        return None

    def draw_for_player_hero_stats(self, steam_id):
        player = self.get_player_by_id(steam_id)
        hero_damage = 'unk' if player.hero_damage is None else player.hero_damage
        items = [ImageCell(item_picture) for item_picture in player.get_item_pictures()]
        # game_mode_name_new_line = '\n'.join(self.game_mode_name.split())

        won_text = ''
        won_color = ''
        if player.won:
            won_text = 'Won'
            won_color = (0, 255, 0)
        else:
            won_text = 'Lost'
            won_color = (255, 0, 0)

        return [
            TextCell(format_unix_to_time(self.start_time), font_size=22),
            TextCell(won_text, font_color=won_color, font_size=28),
            TextCell(self.duration_text, font_size=24),
            TextCell(player.kills, font_size=24),
            TextCell(player.deaths, font_size=24),
            TextCell(player.assists, font_size=24),
            TextCell(hero_damage, font_size=24),
        ] + items
