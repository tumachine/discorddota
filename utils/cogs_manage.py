import asyncio
# from cogs.discord_voice import DiscordVoice
from discord.ext import commands
from abc import ABCMeta, abstractmethod
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
import simpleaudio
from utils.util import get_full_path
import tts.sapi
from index import config
import os
import random
import discord
import pythoncom


class BaseVoice(metaclass=ABCMeta):
    default_voice_path = get_full_path('sounds', 'tmp.wav')
    voice = tts.sapi.Sapi()
    voice.set_voice(config.get_value('voice'))

    @staticmethod
    def stop(bot):
        pass

    @staticmethod
    def play(bot, path):
        pass

    @staticmethod
    def play_text(bot, text):
        pass


class SystemVoice(BaseVoice):
    @staticmethod
    def stop(bot):
        simpleaudio.stop_all()

    @staticmethod
    def play(bot=None, path=BaseVoice.default_voice_path):
        ext = Path(path).suffix[1:]
        sound = AudioSegment.from_file(path, format=ext)
        play(sound)

    @staticmethod
    def play_text(bot=None, text="Temporary"):
        print(text)
        BaseVoice.voice.create_recording(BaseVoice.default_voice_path, text)
        SystemVoice.play(bot)


class DiscVoice(BaseVoice):
    loaded_first_time = True

    @staticmethod
    def play_text(bot, text):
        print(text)
        pythoncom.CoInitialize()
        BaseVoice.voice.create_recording(BaseVoice.default_voice_path, text)
        DiscVoice.play(bot, BaseVoice.default_voice_path)

    @staticmethod
    def play(bot, path=None):
        asyncio.run_coroutine_threadsafe(DiscVoice.play_async(bot, path), bot.loop)

    @staticmethod
    async def play_async(bot: commands.Bot, path=None):
        if path is None:
            path = BaseVoice.default_voice_path

        voice_client = config.get_voice_client(bot)

        voice_channel = config.get_voice_channel_by_id(bot)
        print(f'Current voice channel: {config.get_value("voice_channel")}')

        if DiscVoice.loaded_first_time:
            voice_client_temp = await discord.VoiceChannel.connect(voice_channel)
            await voice_client_temp.disconnect()
            DiscVoice.loaded_first_time = False

        if voice_client is None:
            voice_client = await discord.VoiceChannel.connect(voice_channel)

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path), volume=0.3)
        voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @staticmethod
    def stop(bot):
        voice_client = config.get_voice_client(bot)

        if voice_client is not None:
            if voice_client.is_playing():
                voice_client.stop()


class VoiceManage:
    @staticmethod
    def get_voice(dict_key=None):
        if dict_key is None:
            return DiscVoice

        setting = config.get_value('sound_directions').get(dict_key)
        if setting == "system":
            return SystemVoice
        if setting == "discord":
            return DiscVoice
        return SystemVoice

    @staticmethod
    def get_random_rune_path():
        path = get_full_path('sounds', 'roons')
        sounds = os.listdir(path)
        random_sound = sounds[random.randint(0, len(sounds) - 1)]
        random_sound_path = os.path.join(path, random_sound)
        return random_sound_path
