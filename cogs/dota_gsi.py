from discord.ext import commands

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import asyncio
from utils.util import get_full_path
import keyboard
from utils.text import get_random_fact, convert_seconds_to_human_friendly
from utils.cogs_manage import VoiceManage


class Map:
    game_has_paused = False
    set_time = None
    aegis_expiration_time = None
    roshan_respawn_time = None
    roshan_timer_is_on = False

    def __init__(self, dictionary: dict):
        self.game_time = dictionary['game_time']
        self.clock_time = dictionary['clock_time']
        self.daytime = dictionary['daytime']
        self.nightstalker_night = dictionary['nightstalker_night']
        self.game_state = dictionary['game_state']
        self.paused = dictionary['paused']
        self.win_team = dictionary['win_team']
        self.customgamename = dictionary['customgamename']
        # self.ward_purchase_cooldown = dictionary['ward_purchase_cooldown']

    async def manage_runes_warning(self, bot, before_time=30):
        if self.clock_time > 0:
            if (self.clock_time + before_time) % 300 == 0:
                print(f"Rune warning at: {self.clock_time}")
                VoiceManage.get_voice().play(bot, VoiceManage.get_random_rune_path())

    async def manage_pause(self, bot):
        if not self.paused and Map.game_has_paused:
            # VoiceManage.get_voice().stop(bot)
            print('game has unpaused')
            Map.game_has_paused = False

        if self.paused and not Map.game_has_paused:
            # VoiceManage.get_voice(None).play_text(bot, get_random_fact())
            # VoiceManage.get_voice(None).play(bot, get_full_path('sounds', 'wait', 'jeopardy-theme.mp3'))
            print('game has paused')
            Map.game_has_paused = True

    @staticmethod
    def rosh_is_killed(bot: commands.Bot):
        print('rosh is killed')
        Map.aegis_expiration_time = DotaGSI.des_map.clock_time + 300
        Map.roshan_respawn_time = DotaGSI.des_map.clock_time + 480
        Map.roshan_timer_is_on = True
        Map.set_time = DotaGSI.des_map.clock_time
        VoiceManage.get_voice().play_text(bot, "roshan timer is set")

    @staticmethod
    def disable_roshan_timer(bot):
        print('disable roshan timer')
        Map.roshan_timer_is_on = False
        VoiceManage.get_voice(None).play_text(bot, "roshan timer is disabled")

    @staticmethod
    def time_before_aegis_expires(bot):
        if Map.roshan_timer_is_on:
            aegis_exp_time = Map.aegis_expiration_time - DotaGSI.des_map.clock_time
            if aegis_exp_time >= 0:
                aegis_exp_time_friendly = convert_seconds_to_human_friendly(aegis_exp_time)
                message = f'Aegis will expire in {aegis_exp_time_friendly}'
                VoiceManage.get_voice(None).play_text(bot, message)

    @staticmethod
    def time_before_roshan_respawns(bot):
        if Map.roshan_timer_is_on:
            minimum_respawn_time = Map.roshan_respawn_time - DotaGSI.des_map.clock_time
            if minimum_respawn_time >= 0:
                min_res_time_friendly = convert_seconds_to_human_friendly(minimum_respawn_time)
                message = f'Roshan re spawns in {min_res_time_friendly}'
                VoiceManage.get_voice(None).play_text(bot, message)
            elif minimum_respawn_time >= -180:
                roshan_window = minimum_respawn_time + 180
                roshan_window_friendly = convert_seconds_to_human_friendly(roshan_window)
                message = f'Roshan window is open for {roshan_window_friendly}'
                VoiceManage.get_voice(None).play_text(bot, message)
            else:
                Map.roshan_timer_is_on = False

            # discord_voice = bot.get_cog('DiscordVoice')
            # asyncio.run_coroutine_threadsafe(discord_voice.play_text_recording(message), bot.loop)

    async def manage_roshan_timing(self, bot):
        if Map.roshan_timer_is_on:
            if self.clock_time == Map.aegis_expiration_time - 30:
                print("aegis will expire in 30 seconds")
                VoiceManage.get_voice(None).play_text(bot, "aegis will expire in 30 seconds")
                # discord_voice = bot.get_cog('DiscordVoice')
                # await discord_voice.play_text_recording("aegis will expire in 30 seconds")

            if self.clock_time == Map.roshan_respawn_time:
                print("roshan will respawn in the next 3 minutes")
                VoiceManage.get_voice(None).play_text(bot, "roshan will re spawn in the next 3 minutes")
                # discord_voice = bot.get_cog('DiscordVoice')
                # await discord_voice.play_text_recording("roshan will respawn in the next 3 minutes")


class Server(BaseHTTPRequestHandler):
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message: dict = json.loads(self.rfile.read(length))
        DotaGSI.dmap = message.get('map')


class DotaGSI(commands.Cog):
    dmap = None
    des_map = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.loop.create_task(self.run())

    async def run(self, server_class=HTTPServer, handler_class=Server, port=3000):
        await self.bot.wait_until_ready()
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)

        httpd.socket.settimeout(1)

        print('Launched Dota GSI')
        enabled_first_time = False
        while True:
            httpd.handle_request()
            if DotaGSI.dmap is not None:
                DotaGSI.des_map = Map(DotaGSI.dmap)
                if not enabled_first_time:
                    enabled_first_time = True
                    print('adding hotkeys')
                    keyboard.add_hotkey('shift+k', Map.rosh_is_killed, args=[self.bot])
                    keyboard.add_hotkey('shift+c', Map.time_before_aegis_expires, args=[self.bot])
                    keyboard.add_hotkey('shift+l', Map.disable_roshan_timer, args=[self.bot])
                    keyboard.add_hotkey('shift+v', Map.time_before_roshan_respawns, args=[self.bot])

                await DotaGSI.des_map.manage_runes_warning(self.bot)
                await DotaGSI.des_map.manage_pause(self.bot)
                await DotaGSI.des_map.manage_roshan_timing(self.bot)
            else:
                if enabled_first_time:
                    keyboard.unhook_all_hotkeys()
                    enabled_first_time = False

            await asyncio.sleep(1)


def setup(bot: commands.Bot):
    bot.add_cog(DotaGSI(bot))
