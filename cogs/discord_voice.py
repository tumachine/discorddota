import discord
import tts.sapi
import os
import random
from utils.util import get_full_path
from discord.ext import commands
from index import config
from utils.cogs_manage import VoiceManage


class DiscordVoice(commands.Cog):
    # default_voice_path = get_full_path('sounds', 'tmp.wav')
    # loaded_first_time = True
    #
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        # self.voice = tts.sapi.Sapi()
        # self.voice.set_voice(config.get_value('voice'))
    #
    # async def stop(self):
    #     voice_client = config.get_voice_client(self.bot)
    #
    #     if voice_client is not None:
    #         if voice_client.is_playing():
    #             voice_client.stop()
    #
    # async def play_audio(self, path=default_voice_path):
    #     voice_client = config.get_voice_client(self.bot)
    #
    #     voice_channel = config.get_voice_channel_by_id(self.bot)
    #     print(f'Current voice channel: {config.get_value("voice_channel")}')
    #
    #     if DiscordVoice.loaded_first_time:
    #         voice_client_temp = await discord.VoiceChannel.connect(voice_channel)
    #         await voice_client_temp.disconnect()
    #         DiscordVoice.loaded_first_time = False
    #
    #     if voice_client is None:
    #         # await voice_client.move_to(voice_channel)
    #         voice_client = await discord.VoiceChannel.connect(voice_channel)
    #
    #     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path))
    #     source.volume = 0.5
    #     voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #
    # async def play_text_recording(self, text):
    #     # self.voice.say(text)
    #     self.voice.create_recording(DiscordVoice.default_voice_path, text)
    #     await self.play_audio(DiscordVoice.default_voice_path)

    # def get_random_roons_path(self):
    #     path = get_full_path('sounds', 'roons')
    #     sounds = os.listdir(path)
    #     random_sound = sounds[random.randint(0, len(sounds) - 1)]
    #     random_sound_path = os.path.join(path, random_sound)
    #     return random_sound_path
    #
    # async def play_random_roons(self):
    #     await self.play_audio(self.get_random_roons_path())

    @commands.command()
    async def movevoice(self, ctx: commands.Context, channel=None):
        if channel is None:
            voice_state = ctx.author.voice
            if voice_state is None:
                await ctx.send("You are not connected to any voice channel")
                return
            voice_channel = voice_state.channel

        else:
            voice_channel = config.get_voice_channel(self.bot, channel)
            if voice_channel is None:
                await ctx.send("No voice channel with this name")
                return

        # move voice client to channel
        voice_client = config.get_voice_client(self.bot)
        if voice_client is not None:
            await voice_client.move_to(voice_channel)

        config.change_value('voice_channel', voice_channel.id)
        print(f'Changed to voice channel: {voice_channel.id}')
        message = f"Changed channel to {voice_channel.name}"
        VoiceManage.get_voice().play_text(self.bot, message)
        await ctx.send(message)

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        ctx.voice_client.source.volume = volume
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send('No voice is connected')
        await ctx.voice_client.disconnect()

    @commands.command()
    async def say(self, ctx, message: str):
        VoiceManage.get_voice().play_text(self.bot, message)

    @commands.command()
    async def roons(self, ctx):
        VoiceManage.get_voice().play(self.bot, VoiceManage.get_random_rune_path())

    # @commands.command()
    # async def roons(self, ctx):
    #     await self.play_random_roons()


def setup(bot: commands.Bot):
    bot.add_cog(DiscordVoice(bot))
