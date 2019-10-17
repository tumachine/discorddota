import discord

from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Ready: {self.bot.user} | Guilds: {len(self.bot.guilds)}")

        await self.bot.change_presence(status=discord.Status.online)

    @commands.Cog.listener()
    async def on_command(self, ctx: commands.Context):
        print(f"{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}")


def setup(bot):
    bot.add_cog(Events(bot))
