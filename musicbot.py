# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

# --- DEVELOPED BY KUZEYSHU ---
TOKEN = 'YOUR BOT TOKEN'
COLOR = 0xFF0000 
PREFIX = "."

intents = discord.Intents.default()
intents.message_content = True 
intents.voice_states = True

bot = commands.Bot(
    command_prefix=PREFIX, 
    intents=intents, 
    help_command=None,
    status=discord.Status.idle,
    activity=discord.Game(name=".play <Song Name> | Dev: KuzeyShu")
)

queues = {}

def check_queue(ctx, vc):
    if ctx.guild.id in queues and queues[ctx.guild.id]:
        next_song = queues[ctx.guild.id].pop(0)
        ffmpeg_path = "./ffmpeg.exe" if os.path.exists("./ffmpeg.exe") else "ffmpeg"
        source = discord.FFmpegOpusAudio(
            next_song['url'], 
            executable=ffmpeg_path, 
            before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            options='-vn'
        )
        vc.play(source, after=lambda e: check_queue(ctx, vc))
        embed = discord.Embed(title="🔴 Now Playing", description=f"**{next_song['title']}**", color=COLOR)
        bot.loop.create_task(ctx.send(embed=embed))

YTDL_OPTS = {'format': 'bestaudio/best', 'quiet': True, 'nocheckcertificate': True, 'ignoreerrors': True}

class MusicSelect(discord.ui.Select):
    def __init__(self, options, vc, ctx):
        super().__init__(placeholder="Select a song, my Lord...", options=options)
        self.vc = vc
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        url = self.values[0]
        with yt_dlp.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            song_data = {'url': info['url'], 'title': info['title']}
            if self.vc.is_playing() or self.vc.is_paused():
                if self.ctx.guild.id not in queues: queues[self.ctx.guild.id] = []
                queues[self.ctx.guild.id].append(song_data)
                embed = discord.Embed(title="📝 Added to Queue", description=f"**{info['title']}**", color=COLOR)
                await interaction.followup.send(embed=embed)
            else:
                ffmpeg_path = "./ffmpeg.exe" if os.path.exists("./ffmpeg.exe") else "ffmpeg"
                source = await discord.FFmpegOpusAudio.from_probe(info['url'], executable=ffmpeg_path, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', options='-vn')
                self.vc.play(source, after=lambda e: check_queue(self.ctx, self.vc))
                embed = discord.Embed(title="🔴 Music - Playing", description=f"**{info['title']}**\n\n*Dev: KuzeyShu*", color=COLOR)
                await interaction.followup.send(embed=embed)

class SelectionView(discord.ui.View):
    def __init__(self, options, vc, ctx):
        super().__init__(timeout=60)
        self.add_item(MusicSelect(options, vc, ctx))

@bot.command(name="play")
async def play(ctx, *, search: str = None):
    if not search: return await ctx.send("❌ Enter a song name!")
    if not ctx.author.voice: return await ctx.send("❌ Join a voice channel!")
    vc = ctx.voice_client
    if not vc: vc = await ctx.author.voice.channel.connect()
    msg = await ctx.send(f"🔎 Searching: **{search}**...")
    with yt_dlp.YoutubeDL({'default_search': 'ytsearch5', 'quiet': True}) as ydl:
        info = ydl.extract_info(f"ytsearch5:{search}", download=False)
        entries = info.get('entries', [])
        if not entries: return await msg.edit(content="❌ No results.")
        options = [discord.SelectOption(label=e['title'][:100], value=e['webpage_url']) for e in entries if e]
        embed = discord.Embed(title="Music Search", description=f"Results for: **{search}**", color=COLOR)
        embed.set_footer(text="Developed by KuzeyShu")
        await msg.delete()
        await ctx.send(embed=embed, view=SelectionView(options, vc, ctx))

@bot.command(name="pause")
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Paused.")

@bot.command(name="resume")
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Resumed.")

@bot.command(name="skip")
async def skip(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped.")

@bot.command(name="stop")
async def stop(ctx):
    if ctx.voice_client:
        if ctx.guild.id in queues: queues[ctx.guild.id] = []
        await ctx.voice_client.disconnect()
        await ctx.send("🔴 Disconnected.")

@bot.event
async def on_ready():
    print(f"🔴 {bot.user.name} | Dev: KuzeyShu")

bot.run(TOKEN)