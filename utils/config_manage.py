import json
from discord.ext import commands
import discord
import asyncio


class ConfigManage:
    def __init__(self, file_path):
        with open(file_path, encoding='utf8') as data:
            self.config: dict = json.load(data)

    def change_value(self, value, change_to):
        if not self.config.get(value):
            raise AttributeError()

        self.config[value] = change_to

    def get_value(self, value: str):
        if not self.config.get(value):
            raise AttributeError()

        return self.config[value]

    def get_guild(self, bot: commands.Bot):
        return bot.get_guild(int(self.get_value("guild_id")))

    def get_voice_channel(self, bot, channel_name):
        return discord.utils.get(self.get_guild(bot).voice_channels, name=channel_name)

    def get_voice_channel_by_id(self, bot, channel_id='default'):
        if channel_id == 'default':
            channel_id = int(self.get_value('voice_channel'))
        return discord.utils.get(self.get_guild(bot).voice_channels, id=channel_id)

    def get_voice_client(self, bot):
        return self.get_guild(bot).voice_client


