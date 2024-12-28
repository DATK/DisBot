import discord
from discord.ext import commands
import yt_dlp
import asyncio
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

class MusicPlayer:
    def __init__(self):
        self.current = None
        self.voice_client = None
        self.queue = []
        self.is_paused = False
        self.output = "./"

    async def play_next(self):
        if self.queue:
            self.current = self.queue.pop(0)
            ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }], "noplaylist": True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.current, download=False)
                url = info['url']
                #print(info)
                self.voice_client.play(discord.FFmpegOpusAudio(url, options = "-vn"), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), bot.loop))

    def resume(self):
        if self.is_paused:
            self.voice_client.resume()
            self.is_paused = False
            
    def pause(self):
        if self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_paused = True

    def skip(self):
        if self.voice_client.is_playing():
            self.voice_client.stop()

    def shuffle(self):
        random.shuffle(self.queue)

player = MusicPlayer()

@bot.command(name='join')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        player.voice_client = await channel.connect()
    else:
        await ctx.send("Вы не находитесь в голосовом канале!")

@bot.command(name='leave')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Бот не подключён к голосовому каналу!")

@bot.command(name='play')
async def play(ctx, *, arg):
    player.queue.append(arg)
    if not player.voice_client.is_playing():
        await player.play_next()

@bot.command(name='pause')
async def pause(ctx):
    player.pause()

@bot.command(name='resume')
async def resume(ctx):
    player.resume()

@bot.command(name='skip')
async def skip(ctx):
    player.skip()

@bot.command(name='peremeshka')
async def shuffle(ctx):
    player.shuffle()

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')

bot.run('')