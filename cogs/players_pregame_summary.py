import asyncio
import os
from typing import List

import discord
from PIL import Image
from discord.ext import commands
from prettytable import PrettyTable

from deserialize import StratzPlayer, StratzPlayerHeroPerformances
from index import config, api
from utils.image_cells_manipulation import CellPositionGenerator, TextCell, ImageCell, VerticalCellLines, ColorCell
from utils.images import get_image, get_rank_picture
from utils.ranks import parse_rank_id
from utils.server_log import ServerLog
from utils.text import limit_string_length
from utils.util import get_full_path
from utils.parties import assign_players_party_color
from utils.cogs_manage import VoiceManage
import time


class PlayersPregameSummary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_update())
        self.server_log_path = r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\server_log.txt'

    async def check_update(self):
        await self.bot.wait_until_ready()
        prev_time_file_updated = os.stat(self.server_log_path)[8]
        print("Launched pregame_summary_cog")
        while True:
            time_file_updated = os.stat(self.server_log_path)[8]
            if time_file_updated != prev_time_file_updated:
                prev_time_file_updated = time_file_updated
                server_log = ServerLog(self.get_last_line(self.server_log_path))
                if server_log.is_match():
                    print('new match detected')
                    await self.send_player_info(server_log)

            await asyncio.sleep(5)

    async def send_player_info(self, server_log: ServerLog):
        await self.bot.wait_until_ready()
        start_time = time.time()
        players = await api.build_async_request(api.get_stratz_player, server_log.players_lobby)
        players_hero_performance = await api.build_async_request(api.get_stratz_player_hero_performance, server_log.players_lobby)
        players_party_color = await assign_players_party_color(server_log.players_lobby, 5, 2)
        print(f"30 api calls in {time.time() - start_time}")

        p = PlayersPregameSummaryData(server_log, players, players_hero_performance, players_party_color)
        text = p.generate_text()
        text_channel_id = config.get_value('text_channel')
        text_channel = self.bot.get_channel(int(text_channel_id))
        await p.play_voice_highest_rank_player(self.bot)
        p.generate_image()
        await text_channel.send(file=discord.File(get_full_path('images', 'tmp.png')))
        # await text_channel.send(text, file=discord.File(get_full_path('images', 'tmp.png')))

    def get_last_line(self, path: str):
        with open(path, "rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
            last = f.readline()
            return last.decode('ascii')


class PlayersPregameSummaryPlayerData:
    def __init__(self, player, hero_performance, color):
        self.hero_performance = StratzPlayerHeroPerformances(hero_performance)
        self.color = color
        self.stratz_player = StratzPlayer(player)
        self.name = limit_string_length(self.stratz_player.name, 13)
        self.rank, self.previous_rank = self.stratz_player.get_current_and_previous_rank()

    def for_image(self):
        # hero_performances = StratzPlayerHeroPerformances(api.get_stratz_player_hero_performance(self.stratz_player.steam_id))
        hero_ids = [hero_performance.hero_id for hero_performance in self.hero_performance.sort_by_best(3)]

        heroes = []
        for hero_id in hero_ids:
            heroes.append(ImageCell(Image.open(get_full_path('images', 'heroes', f"{hero_id}.jpg"))))

        return [
            ImageCell(get_image(self.stratz_player.avatar_full)),
            ColorCell(self.color),
            TextCell(self.name),
            ImageCell(get_rank_picture(self.rank)),
            ImageCell(get_rank_picture(self.previous_rank)),
            TextCell(f"{self.stratz_player.match_count}\n{self.stratz_player.winrate}%"),
            heroes[0], heroes[1], heroes[2]
        ]

    def for_text(self):
        return [
            self.name,
            parse_rank_id(int(self.rank)),
            parse_rank_id(int(self.previous_rank)),
            self.stratz_player.leaderboard_rank,
            self.stratz_player.get_formatted_time(),
            self.stratz_player.match_count,
            self.stratz_player.winrate
        ]


class PlayersPregameSummaryData:
    def __init__(self, server_log: ServerLog, players, players_hero_performance, players_party_color):
        self.players: List[PlayersPregameSummaryPlayerData] = []
        # players_party_color = assign_players_party_color(server_log.players_lobby, 5, 2)
        for count, player in enumerate(server_log.players_lobby):
            self.players.append(PlayersPregameSummaryPlayerData(players[count], players_hero_performance[count], players_party_color[count]))

    async def play_voice_highest_rank_player(self, bot):
        highest_player_rank, rank = self.get_highest_rank_player()

        # discord_voice = bot.get_cog('DiscordVoice')
        # await discord_voice.play_text_recording(f"The highest player has name of {highest_player_rank.name}, "
        #                                         f"the rank is {parse_rank_id(int(rank))}")
        text = f"The highest player has name of {highest_player_rank.name}, the rank is {parse_rank_id(int(rank))}"
        VoiceManage.get_voice(None).play_text(bot, text)

    def get_highest_rank_player(self):
        # highest_rank_player = sorted(self.players, key=lambda k: int(k.rank), reverse=True)[0]
        highest_rank_player = max(self.players, key=lambda k: int(k.rank))
        highest_previous_rank_player = max(self.players, key=lambda k: int(k.previous_rank))

        if highest_previous_rank_player.previous_rank > highest_rank_player.rank:
            return highest_previous_rank_player, highest_previous_rank_player.previous_rank
        return highest_rank_player, highest_rank_player.rank

    def generate_image(self):
        img = Image.open(get_full_path('images', 'templates', 'PlayersPregameSummary.png'))

        cell_lines = VerticalCellLines(
                        CellPositionGenerator(x_start=246, y_start=89,
                                              columns=[100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                                              column_spaces=[10, 10, 10, 10, 10, 20, 10, 10, 10, 10],
                                              rows=[90, 10, 60, 100, 100, 60, 60, 60, 60],
                                              row_spaces=[10, 0, 20, 20, 20, 20, 20, 0, 0])
        )

        img = cell_lines.draw([player.for_image() for player in self.players], img)
        img.save(get_full_path('images', 'tmp.png'))

    def generate_text(self):
        summary = PrettyTable()
        summary.field_names = ['Name', 'Rank', 'Prev Rank', 'Leaderboard', 'First Match', 'Matches', 'Winrate']
        summary.align['Name'] = 'l'
        summary.align['Rank'] = 'l'
        summary.align['Prev Rank'] = 'l'

        for counter, player in enumerate(self.players):
            if counter == 5:
                summary.add_row(['', '', '', '', '', '', ''])
            summary.add_row(player.for_text())

        return f"```{summary.get_string()}```"


def setup(client: commands.Bot):
    client.add_cog(PlayersPregameSummary(client))
