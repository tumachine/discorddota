#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The base URL and the API calls are defined in this file"""

BASE_URL = "http://api.steampowered.com/"
GET_MATCH_HISTORY = "IDOTA2Match_570/GetMatchHistory/v001/"
GET_MATCH_HISTORY_BY_SEQ_NUM = "IDOTA2Match_570/GetMatchHistoryBySequenceNum/v0001/"
GET_MATCH_DETAILS = "IDOTA2Match_570/GetMatchDetails/v001/"
GET_LEAGUE_LISTING = "IDOTA2Match_570/GetLeagueListing/v0001/"
GET_LIVE_LEAGUE_GAMES = "IDOTA2Match_570/GetLiveLeagueGames/v0001/"
GET_TEAM_INFO_BY_TEAM_ID = "IDOTA2Match_570/GetTeamInfoByTeamID/v001/"
GET_PLAYER_SUMMARIES = "ISteamUser/GetPlayerSummaries/v0002/"
GET_HEROES = "IEconDOTA2_570/GetHeroes/v0001/"
GET_GAME_ITEMS = "IEconDOTA2_570/GetGameItems/v0001/"
GET_TOURNAMENT_PRIZE_POOL = "IEconDOTA2_570/GetTournamentPrizePool/v1/"
GET_TOP_LIVE_GAME="IDOTA2Match_570/GetTopLiveGame/v1/"
BASE_ITEMS_IMAGES_URL = 'http://cdn.dota2.com/apps/dota2/images/items/'
BASE_HERO_IMAGES_URL = 'http://cdn.dota2.com/apps/dota2/images/heroes/'

GET_FRIENDS_LIST = 'ISteamUser/GetFriendList/v0001/'

OPEN_DOTA_BASE_URL = "https://api.opendota.com/api/"
OPEN_MATCHES = "matches/{}"
OPEN_PLAYER = "players/{}/"
OPEN_PLAYER_WL = "players/{}/wl/"
OPEN_PLAYER_RECENT_MATCHES = "players/{}/recentMatches/"
OPEN_PLAYER_MATCHES = "players/{}/matches/"
OPEN_PLAYER_HEROES = "players/{}/heroes/"
OPEN_PLAYER_PEERS = "players/{}/peers/"
OPEN_PLAYER_PROS = "players/{}/pros/"
OPEN_PLAYER_TOTALS = "players/{}/totals/"
OPEN_PLAYER_COUNTS = "players/{}/counts/"
OPEN_PLAYER_HISTOGRAMS = "players/{}/histograms/{}/"
OPEN_PLAYER_WARDMAP = "players/{}/wardmap/"
OPEN_PLAYER_WORDCLOUD = "players/{}/wordcloud/"
OPEN_PLAYER_RATINGS = "players/{}/ratings/"
OPEN_PLAYER_RANKINGS = "players/{}/rankings/"

STRATZ_BASE_URL = "https://api.stratz.com/api/v1/"
STRATZ_PLAYER = "player/{}/"
STRATZ_PLAYERS = "player/"
STRATZ_PLAYER_MATCHES = "player/{}/matches/"
STRATZ_PLAYER_CARDS = "player/{}/cards/"
STRATZ_PLAYER_PERFORMANCE = "player/{}/performance/"
STRATZ_PLAYER_HERO_PERFORMANCE = "player/{}/heroPerformance/"
STRATZ_PLAYER_SINGLE_HERO_PERFORMANCE = "player/{}/heroPerformance/{}/"
STRATZ_PLAYER_BEHAVIOR_CHART = "player/{}/behaviorChart/"
STRATZ_PLAYER_SEASON_LEADERBOARD = "player/seasonLeaderBoard/"
STRATZ_PLAYER_HISTORY = "player/{}/history/"
STRATZ_PLAYER_CARD_HOVER = "player/{}/cardHover/"
STRATZ_PLAYER_DOTAPLUS_LEADERBOARD = "player/dotaPlusLeaderboard/"
STRATZ_PLAYER_PRO_STEAM_ACCOUNT = "player/proSteamAccount/"
STRATZ_PLAYER_BATTLEPASS_LEADERBOARD = "player/battlePassLeaderboard/"
STRATZ_PLAYER_PLAYED_WITH_PRO = "player/{}/playedWithPro/"
STRATZ_PLAYER_SUMMARY = "player/{}/summary/"

STRATZ_DRAFT = "Draft/"
STRATZ_DRAFT_HERO_HIGHLIGHT = "Draft/{}/heroHighlight/"
STRATZ_DRAFT_HERO_WEIGHT = "Draft/heroWeight/"

STRATZ_MATCH = "match/{}/"
STRATZ_MATCHES = "match/"
STRATZ_MATCH_BREAKDOWN = "match/{}/breakdown/"