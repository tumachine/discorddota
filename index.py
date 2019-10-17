import os

from discord.ext import commands

from dota2api import Initialise
from utils.config_manage import ConfigManage
from utils.util import get_full_path

# DAVID
# ZIRA
# IRINA


config = ConfigManage(get_full_path('config_test.json'))
api = Initialise(config.get_value('api_key'))
bot = commands.Bot(command_prefix=config.get_value('prefix'))


if __name__ == "__main__":
    for file in os.listdir("cogs"):
        if file.endswith('.py'):
            name = file[:-3]
            bot.load_extension(f'cogs.{name}')

    bot.run(config.get_value('token'))

# channel = self.bot.get_channel(532657285923864608)
# guild = self.bot.get_guild(532657285923864606)
# test_channel = 53265728592386460811111
# main_channel = 199929173521727501

# bot can turn other features on and off
# text-to-speech
#   enable/disable runes notifications
#   enable/disable highest player warning notification
#   !settings runes on
#   !settings playerwarning on
#
#
# information about pregame-summary and postgame summary
# can be presented in two forms
#   text: easier on processing power
#   picture: pretty but slow
#   we want to have an ability to present information in either text or picture
#   !settings picture on
#   !settings picture off
#   when picture is set to on, text will not be shown
#   when off, only text will show


# abilities['abilities']:
# 'id'

# https://discordapp.com/oauth2/authorize?client_id={CLIENTID}&scope=bot&permissions={PERMISSIONINT}


# API_KEY = '7CB8779F71A78DDE9712E590674E9333'
# token = "NTMyNjU3Njk1MzA4NjQ0MzY3.DypdSQ.MMwKl8ToVW4milJ5E96ClLIVqVs"
