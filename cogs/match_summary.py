import discord
from PIL import Image
from discord.ext import commands
from prettytable import PrettyTable

from DB.user import ManageUser
from deserialize import MatchDetails, StratzPlayer, PlayerSummaries, Player
from index import api
from utils.image_cells_manipulation import CellPositionGenerator, TextCell, ImageCell, HorizontalCellLines, CellPosition
from utils.images import get_item_picture, get_rank_picture, get_image
from utils.ranks import parse_rank_id
from utils.text import limit_string_length, parse_int_to_thousands_k
from utils.util import get_full_path, replace_dict_null


class MatchSummary(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def lastmatch(self, ctx: commands.Context):
        user = ManageUser.load(ctx.message.author)
        if not user:
            return 'Not registered, to register type !connect steam_id'
        match = api.get_match_history(user.steam_id, matches_requested=1)['matches'][0]
        user.update_last_match(match['match_id'])
        # get players account ids
        await self.get_match_summary(match['match_id'], ctx.channel)

    @commands.command()
    async def match(self, ctx: commands.Context, match_id: int):
        await self.get_match_summary(match_id, ctx.channel)

    async def get_match_summary(self, match_id: int, channel):
        self.bot.get_all_channels()
        match_summary_data = MatchSummaryData(match_id)
        match_summary_data.generate_image()
        text = match_summary_data.generate_text()

        await channel.send(text, file=discord.File(get_full_path('images', 'tmp.png')))


class MatchSummaryPlayerData:
    def __init__(self, player):
        self.player = player
        players = PlayerSummaries(api.get_player_summaries(self.player.account_id)).players
        player_summary = {}
        player_stratz = {}
        if players:
            player_summary = players[0].dict
            player_stratz = api.get_stratz_player(self.player.account_id)
        player_summary = Player(replace_dict_null(['personaname'], ['Unknown'], player_summary))
        player_stratz = StratzPlayer(replace_dict_null(['ranks', 'avatarMedium'], [[], 'unknown'], player_stratz))

        self.name = player_summary.personaname

        # value if not exists - unknown
        self.avatar_medium = player_stratz.avatar_medium
        self.rank, self.previous_rank = player_stratz.get_current_and_previous_rank()

    def for_image(self):
        if self.avatar_medium == 'unknown':
            profile_picture = Image.open(get_full_path('images', 'steam', 'default_image.png'))
        else:
            profile_picture = get_image(self.avatar_medium)

        name = limit_string_length(self.name, 10)
        hero = Image.open(get_full_path('images', 'heroes', f"{self.player.hero_id}.jpg"))
        rank = get_rank_picture(self.rank)
        prev_rank = get_rank_picture(self.previous_rank)
        hero_damage = parse_int_to_thousands_k(self.player.hero_damage)
        items = [ImageCell(get_item_picture(item_id)) for item_id in self.player.get_item_ids()]
        return [
               ImageCell(profile_picture),
               TextCell(name, font_size=22),
               ImageCell(hero),
               ImageCell(rank),
               ImageCell(prev_rank),
               TextCell(self.player.kills, font_size=22),
               TextCell(self.player.deaths, font_size=22),
               TextCell(self.player.assists, font_size=22),
               TextCell(hero_damage)
        ] + items

    def for_text(self):
        hero_name = limit_string_length(self.player.get_hero_name(), 10)

        return [
            limit_string_length(self.name, 13), hero_name,
            parse_rank_id(int(self.rank)), parse_rank_id(int(self.previous_rank)),
            self.player.level,
            self.player.kills, self.player.deaths, self.player.assists,
            self.player.last_hits,
            self.player.gold_per_min,
            parse_int_to_thousands_k(self.player.hero_damage),
            parse_int_to_thousands_k(self.player.gold)
        ]


class MatchSummaryData:
    def __init__(self, match_id):
        self.match_details = MatchDetails(api.get_match_details(match_id))

        self.players = [MatchSummaryPlayerData(player) for player in self.match_details.players]

    def generate_image(self):
        img = Image.open(get_full_path('images', 'templates', 'PostgameSummaryTest.png'))

        side_won_color = (0, 200, 0) if self.match_details.radiant_win else (200, 0, 0)
        side_won_cell = TextCell(self.match_details.side_won_text, font_size=36, font_color=side_won_color)
        side_won_cell.draw(img, CellPosition(360, 120, 20, 160))

        radiant_score_cell = TextCell(self.match_details.radiant_score, font_size=45, font_color=(0, 200, 0))
        radiant_score_cell.draw(img, CellPosition(140, 80, 120, 380))

        dire_score_cell = TextCell(self.match_details.dire_score, font_size=45, font_color=(200, 0, 0))
        dire_score_cell.draw(img, CellPosition(140, 80, 120, 650))

        duration_cell = TextCell(self.match_details.duration_text, font_size=40)
        duration_cell.draw(img, CellPosition(180, 100, 110, 500))

        # no need to generate it each time, would be enough to save it in memory or disk
        cell_lines = HorizontalCellLines(
            CellPositionGenerator(x_start=400, y_start=140,
                                  columns=[100, 220, 100, 100, 100, 40, 40, 40, 100, 100, 100, 100, 100, 100, 100],
                                  column_spaces=[10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0, 0],
                                  rows=[60, 60, 60, 60, 60, 60, 60, 60, 60, 60],
                                  row_spaces=[10, 20, 20, 20, 20, 170, 20, 20, 20, 20])
        )

        players = [player.for_image() for player in self.players]
        cell_lines.draw(players, img)
        img.save(get_full_path('images', 'tmp.png'))

    def generate_text(self) -> str:
            players_match_summary = f"{self.match_details.side_won_text} Radiant: {self.match_details.radiant_score} " \
                                    f"Dire: {self.match_details.dire_score}  Duration: {self.match_details.duration}"

            summary = PrettyTable()
            summary.field_names = ['Player', 'Hero', 'Rank', 'Prev Rank', 'LVL', 'K', 'D', 'A',
                                   'LH', 'GPM', 'HD', 'G']

            summary.align['Player'] = 'l'
            summary.align['Rank'] = 'l'
            summary.align['Prev Rank'] = 'l'
            summary.align['Hero'] = 'l'

            for player in self.players:
                summary.add_row(player.for_text())

            return f"```{players_match_summary}\n{summary.get_string()}```"


def setup(bot):
    bot.add_cog(MatchSummary(bot))

