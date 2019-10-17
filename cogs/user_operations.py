from discord.ext import commands

from dota2api.src.exceptions import APIError
from DB.user import ManageUser
from index import api


class UserOperations(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def count(self, ctx):
        await ctx.send(ctx.guild.member_count)

    @commands.command()
    async def connect(self, ctx, steam_id: int):
        try:
            api.get_player_summaries([steam_id])
        except IndexError:
            await ctx.send(f"Steam id {steam_id} doesn't exist")
            return

        user = ManageUser.load(ctx.message.author)
        if user is not None and user.steam_id == steam_id:
            await ctx.send(f"You are already registered under {steam_id} id")
            return

        try:
            matches = api.get_match_history(steam_id)['matches'][0]
        except APIError:
            await ctx.send('User with that steam_id hidden his profile')
            return

        if user is not None:
            await ctx.send(user.update(steam_id, matches['match_id']))
        await ctx.send(ManageUser.insert(ctx.message.author, steam_id, matches['match_id']))


def setup(bot: commands.Bot):
    bot.add_cog(UserOperations(bot))

