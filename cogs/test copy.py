import discord
import os, datetime
from yt_dlp import YoutubeDL
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!')

players = {}

# Function to get the audio source for a YouTube video and
# Extract audio from YouTube video using yt_dlp
class ytdlp_logger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def Error(self, msg):
        print(f"Error: {msg}")
        
def music_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def get_audio_source(url):
    global audio_title
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
        'quiet': True,
        'no_warnings': True,
        'logger': 'ytdl_hook_logger',
        'logger': ytdlp_logger(),
        'progress_hooks': [music_hook],
        'outtmpl': 'audio.%(ext)s',
        'default_search': 'ytsearch:',
        'source_address': '0.0.0.0',
        'socket_timeout': 900,
        'socket_io_timeout': 900,
        'noplaylist': True,
        'simulate': True,
        'audioformat': 'mp3',
        'listformats': False,
        'retries': 10,
        'retry_max_sleep': 60,
        'verbose': False,
        'ignore❌ Errors': True,
        'socket_timeout': 10,
        'socket_io_timeout': 10,
        'nocheckcertificate': True,
        'cookiefile': None,
        'proxy': None,
        'proxy_username': None,
        'proxy_password': None,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
        'format': 'bestaudio/best',
        'verbose': False,
        'socket_timeout': 10,
        'socket_io_timeout': 10,
        'nocheckcertificate': True,
        'cookiefile': None,
        'proxy': None,
        'proxy_username': None,
        'proxy_password': None,
        'ffmpeg_location': 'ffmpeg/ffmpeg.exe'
    }
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict['url']
        audio_title = info_dict['title']
        print(f"Audio source: {audio_title}")
        print(f"Audio source: {url}")
        return discord.FFmpegOpusAudio(audio_url, **FFMPEG_OPTIONS)

# Play command to play the audio in the voice channel
def is_playlist(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return 'entries' in info

def get_playlist_urls(url):
    with YoutubeDL() as ydl:
        try:
            playlist = ydl.extract_info(url, download=False)
            playlist_urls = []
            for entry in playlist['entries']:
                if entry:
                    playlist_urls.append(entry['webpage_url'])
            return playlist_urls
        except Exception as e:
            print(f"Error extracting playlist URLs: {e}")
            return []

    
queues = {}

@bot.slash_command()
async def play(ctx, url):
    if not ctx.author.voice:
        embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        return
    else:
        channel = ctx.author.voice.channel
    try:
        await channel.connect()
    except:
        pass
    guild = ctx.guild
    audio_source = get_audio_source(url)
    if guild.voice_client.is_playing():
        print("currently playing so add to queue")
        if guild.id not in queues:
            queues[guild.id] = []
        queues[guild.id].append((url, len(queues[guild.id]) + 1))
        embed = discord.Embed(title="Added to queue", description=f"Position: {len(queues[guild.id])}", color=0x00FF00)
        await ctx.response.send_message(embed=embed, ephemeral=True)
    else:
        player = guild.voice_client.play(audio_source, after=lambda e: on_player_finished(guild, ctx))
        players[guild.id] = player
        print(f"Playing audio for {url}")


def on_player_finished(guild, ctx):
    if guild.id in queues and len(queues[guild.id]) > 0:
        url, pos = queues[guild.id].pop(0)
        audio_source = get_audio_source(url)
        player = guild.voice_client.play(audio_source, after=lambda e: on_player_finished(guild, ctx))
        players[guild.id] = player
        embed = discord.Embed(title="Now Playing", description=f"{url} (Position: {pos})", color=0x00FF00)
        ctx.channel.send(embed=embed)
        print(f"Playing audio for {url}")
    else:
        guild.voice_client.disconnect()
        players.pop(guild.id)
        print("Disconnected from voice channel")

@bot.slash_command()
async def queue(ctx):
    guild = ctx.guild
    if guild.id not in queues or not queues[guild.id]:
        embed = discord.Embed(title="Queue", description="The queue is empty", color=0xFFB6C1)
        await ctx.send(embed=embed)
    else:
        queue_str = "Current music queue:\n"
        for queue_num in queues[guild.id]:
            queue_str += f"{queue_num}. {audio_title}\n"
        embed = discord.Embed(title="Queue", description=queue_str, color=0xFFB6C1)
        await ctx.send(embed=embed)

@bot.slash_command()
async def skip(ctx):
    guild = ctx.guild
    if not ctx.author.voice:
        embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        return
    if guild.voice_client:
        if guild.voice_client.is_playing():
            guild.voice_client.stop()
            print("Audio skipped")
            if guild.id in queues and queues[guild.id]:
                url, queue_num = queues[guild.id].pop(0)
                audio_source = get_audio_source(url)
                player = guild.voice_client.play(audio_source)
                players[guild.id] = player
                embed = discord.Embed(title="✅Skipped", description=f"Playing {url} (queue position {queue_num})", color=0x00FF00)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="⚠️ Queue", description="No more songs in queue", color=0xFFB6C1)
                await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="❌ Error", description="Not currently playing audio", color=0xFF0000)
            await ctx.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)

# Pause command to pause the audio in the voice channel
@bot.slash_command()
async def pause(ctx):
    guild = ctx.guild
    if not ctx.author.voice:
        embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        return
    if guild.voice_client:
        if guild.voice_client.is_playing():
            guild.voice_client.pause()
            print(f"{audio_title} paused")
            embed = discord.Embed(
                title=f"✅ {audio_title} Paused",
                color=0xFFB6C1,
            )
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx.send("Not currently playing audio")
    else:
        embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)

# Resume command to resume the audio in the voice channel
@bot.slash_command()
async def resume(ctx):
    guild = ctx.guild
    if not ctx.author.voice:
        embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)
        return
    if guild.voice_client:
        if guild.voice_client.is_paused():
            guild.voice_client.resume()
            print(f"{audio_title} Resumed")
            embed = discord.Embed(
                title=f"✅ {audio_title} resumed",
                color=0xFFB6C1,
            )
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx.send("Not currently paused")
    else:
        embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)

# Stop command to stop the audio in the voice channel and disconnect
@bot.slash_command()
async def stop(ctx):
    guild = ctx.guild
    if guild.voice_client:
        if guild.voice_client.is_connected():
            await guild.voice_client.disconnect()
            print("Audio stopped and disconnected")
            embed = discord.Embed(
                title="✅ Audio stopped and disconnected",
                color=0xFFB6C1,
            )
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx.send("Not currently connected to a voice channel")
    else:
        embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
        await ctx.response.send_message(embed=embed, ephemeral=True)


bot.run(os.getenv('DISCORD_TOKEN'))
