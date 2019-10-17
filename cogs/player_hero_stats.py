from discord.ext import commands
from dota2api.src.parse import get_by_id
from index import api
from DB.user import ManageUser
from deserialize.match_history import MatchHistory
from deserialize.match_details import MatchDetails
from deserialize.player_summaries import PlayerSummaries

from typing import List

from utils.util import get_full_path
from PIL import Image
from utils.image_cells_manipulation import ImageCell, TextCell, CellPosition, HorizontalCellLines, VerticalCellLines, CellPositionGenerator
import discord
import asyncio


class PlayerHeroStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def heroguide(self, ctx, hero_name: str):
        hero_id = get_by_id.get_hero_id_by_name(hero_name)
        if hero_id == -1:
            await ctx.send('No hero with this name')
            return
        await ctx.send(f"https://www.dotabuff.com/heroes/{hero_name}/guides")

    @commands.command()
    async def hero(self, ctx, hero_name: str):
        user = ManageUser.load(ctx.message.author)
        if not user:
            await ctx.send('Not registered, to register type !connect steam_id')
            return

        hero_id = get_by_id.get_hero_id_by_name(hero_name)
        if hero_id == -1:
            await ctx.send('No hero with this name')
            return

        match_hero_history = MatchHistory(api.get_match_history(user.steam_id, hero_id=hero_id))
        if match_hero_history.num_results < 5:
            await ctx.send('You have less than 5 games played on this hero, I cannot currently provide stats for that')
            return

        matches = []
        match_ids = []
        for count, match in enumerate(match_hero_history.matches):
            if count == 5:
                break
            matches.append(MatchDetails(api.get_match_details(match.match_id)))
            # match_ids.append(match.match_id)
        # matches = asyncio.run_coroutine_threadsafe(api.build_async_request(api.get_match_details, match_ids, get_url=None), self.bot.loop).result()
        # des_matches = [MatchDetails(match) for match in matches]
            # matches.append(MatchDetails(api.get_match_details(match.match_id)))

        PlayerHeroStatsData(matches, hero_id, hero_name, user.steam_id).generate_image()
        # PlayerHeroStatsData(matches, hero_id, hero_name, user.steam_id).generate_image()
        await ctx.channel.send(file=discord.File(get_full_path('images', 'tmp.png')))


class PlayerHeroStatsData:
    def __init__(self, matches: List[MatchDetails], hero_id, hero_name, steam_id):
        self.matches = matches
        self.hero_id = hero_id
        self.hero_name = hero_name
        self.steam_id = steam_id

    def generate_image(self):
        img = Image.open(get_full_path('images', 'templates', 'PlayerHeroStatsTest.png'))

        # title_cell = TextCell(20, 20, 1610, 60)
        player_summary = PlayerSummaries(api.get_player_summaries(self.steam_id))
        title_cell = TextCell(f"Hero summary for {player_summary.players[0].personaname}", font_size=24)
        title_cell.draw(img, CellPosition(1610, 60, 20, 20))

        hero_image = Image.open(get_full_path('images', 'heroes', f"{self.hero_id}.jpg"))
        hero_cell = ImageCell(hero_image)
        hero_cell.draw(img, CellPosition(300, 280, 20, 100))

        hero_name_cell = TextCell(self.hero_name, font_size=22)
        hero_name_cell.draw(img, CellPosition(300, 100, 20, 400))

        # no need to generate it each time, would be enough to save it in memory or disk
        cell_lines = HorizontalCellLines(
            CellPositionGenerator(x_start=340, y_start=140,
                                  columns=[100, 100, 100, 40, 40, 40, 100, 100, 100, 100, 100, 100, 100],
                                  column_spaces=[15, 25, 20, 20, 20, 20, 20, 20, 0, 0, 0, 0, 0],
                                  rows=[60, 60, 60, 60, 60],
                                  row_spaces=[10, 20, 20, 20, 20])
        )

        players = [match.draw_for_player_hero_stats(self.steam_id) for match in self.matches]
        cell_lines.draw(players, img)
        img.save(get_full_path('images', 'tmp.png'))


def setup(bot: commands.Bot):
    bot.add_cog(PlayerHeroStats(bot))
