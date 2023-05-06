
import discord
import os, datetime, asyncio,math
from yt_dlp import YoutubeDL

from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.ext import commands



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
        print(f"Audio source: {url}")
        return discord.FFmpegOpusAudio(audio_url, **FFMPEG_OPTIONS)
    
def get_audio_title(url):
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
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_title = info_dict['title']
        return audio_title
    
# def get_audio_source(url):
#     global audio_title
#     ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
#     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#     with YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         audio_url = info_dict['url']
#         audio_title = info_dict['title']
#         print(f"Audio source: {audio_title}")
#         print(f"Audio source: {url}")
#         return discord.FFmpegOpusAudio(audio_url, **FFMPEG_OPTIONS)

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
            return 
        
# async def load_next_track(self, guild, ctx):
#     if guild.id in queues and len(queues[guild.id]) > 0:
#         global audio_title
#         url, audio_title, pos = queues[guild.id].pop(0)
#         audio_source = get_audio_source(url)
#         player = guild.voice_client.play(audio_source, after=lambda e: Music.on_player_finished(self, guild, ctx, audio_title))
#         players[guild.id] = player
#         embed = discord.Embed(title="⏯️ Now Playing", description=f"Currently Playing: {audio_title}", color=0x00FF00)
#         await ctx.send(embed=embed)
#         print(f"Playing audio for {url}")

#         # Update positions of remaining songs in the queue
#         for i, (url, title, position) in enumerate(queues[guild.id], start=1):
#             if position <= pos:
#                 position -= 1
#             queues[guild.id][i-1] = (url, title, position)

#     else:
#         embed = discord.Embed(
#             title="👋 Queue Finished",
#             description="I have finished playing all the songs in the queue and am leaving the voice channel. Thank you for listening!",
#             color=0xFFB6C1,
#         )
#         await ctx.send(embed=embed)
#         await guild.voice_client.disconnect()
#         players.pop(guild.id)

players = {}
queues={}
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.curr_tracks = {}
        self.skip_votes = {}
        self.last_skipper = None

    music = SlashCommandGroup("music", "Music Commands!")
    
    async def load_next_track(self, guild, ctx):
        curr_track = self.curr_tracks[guild.id]
        if guild.id not in self.skip_votes:
            self.skip_votes[guild.id] = []
        if guild.id in self.skip_votes and len(self.skip_votes[guild.id]) >= len(guild.voice_client.channel.members) / 2 and len(guild.voice_client.channel.members) >= 1:
            print("clearing queu")
            self.skip_votes[guild.id] = []
            queues[guild.id].pop(0)
            for i in range(len(queues[guild.id])):
                queues[guild.id][i] = (queues[guild.id][i][0], queues[guild.id][i][1], queues[guild.id][i][2]-1)
            if len(queues[guild.id]) > 0:
                url, audio_title, pos = queues[guild.id][0]
                audio_source = get_audio_source(url)
                try:
                    player = guild.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.on_player_finished(guild, ctx, audio_title), self.bot.loop))
                except discord.errors.ClientException as e:
                    print(f"Error: {e}")
                else:
                    players[guild.id] = player
                    self.curr_tracks[guild.id] = (url, audio_title)
                    embed = discord.Embed(title="⏯️ Now Playing", description=f"Currently Playing: {audio_title}", color=0x00FF00)
                    await ctx.send(embed=embed)
                    print(f"Playing audio for {url}")
                    print("Load next track",queues)
            if len(queues[guild.id]) == 0:
                audio_title = self.curr_tracks[guild.id][1]
                embed = discord.Embed(
                    title="👋 Queue Finished",
                    description=f"I have finished playing all the songs in the queue and am leaving the voice channel. Thank you for listening to {audio_title}!",
                    color=0xFFB6C1,
                )
                await ctx.send(embed=embed)
                await guild.voice_client.disconnect()
                players.pop(guild.id)
                self.curr_tracks.pop(guild.id)
        elif guild.voice_client.is_playing():
            pass
        # If the song has finished playing, remove it from the queue and load the next one
        else:
            queues[guild.id].pop(0)
            for i in range(len(queues[guild.id])):
                queues[guild.id][i] = (queues[guild.id][i][0], queues[guild.id][i][1], queues[guild.id][i][2]-1)
            if len(queues[guild.id]) > 0:
                url, audio_title, pos = queues[guild.id][0]
                audio_source = get_audio_source(url)
                try:
                    player = guild.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.on_player_finished(guild, ctx, audio_title), self.bot.loop))
                except discord.errors.ClientException as e:
                    print(f"Error: {e}")
                else:
                    players[guild.id] = player
                    self.curr_tracks[guild.id] = (url, audio_title)
                    embed = discord.Embed(title="⏯️ Now Playing", description=f"Currently Playing: {audio_title}", color=0x00FF00)
                    await ctx.send(embed=embed)
                    print(f"Playing audio for {url}")
                    print("Load next track",queues)
            else:
                audio_source = get_audio_source(url)
                audio_title = get_audio_title(url)
                players[guild.id] = guild.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.on_player_finished(guild, ctx, audio_title), self.bot.loop))
                queues[guild.id] = [(url, audio_title, 1)]
                embed = discord.Embed(title="⏯️ Now Playing", description=f"Currently Playing: {audio_title}", color=0x00FF00)
                await ctx.send(embed=embed)

                # load the next track in the queue
                self.bot.loop.create_task(self.load_next_track(guild, ctx))

    
    async def on_player_finished(self, guild, ctx, audio_title):
        print(f"Finished playing audio for {audio_title}")
        # Load the next track in the queue
        await self.load_next_track(guild, ctx)

    
    async def skip_to_next_track(self, guild, ctx):
        # Get the guild's audio player
        player = players.get(guild.id)
        if not player:
            return
        # Stop playing the current track
        player.stop()
        # Check if the user has already voted to skip
        if ctx.author.id in self.skip_votes.get(guild.id, []):
            embed = discord.Embed(title="❌ Error", description="You have already voted to skip this track", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Add the user's ID to the list of skip votes for this guild
        if guild.id not in self.skip_votes:
            self.skip_votes[guild.id] = []
        self.skip_votes[guild.id].append(ctx.author.id)
        # Load the next track in the queue
        await self.load_next_track(guild, ctx)

    @music.command()
    async def play(self, ctx, *, url):
        if not ctx.author.voice:
            embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        guild = ctx.guild
        audio_title = get_audio_title(url)
        audio_source = get_audio_source(url)
        if guild.voice_client is None:
            await ctx.author.voice.channel.connect()
        if guild.id not in queues:
            queues[guild.id] = []
        if guild.voice_client.is_playing():
            # Add the requested song to the queue
            queues[guild.id].append((url, audio_title, len(queues[guild.id]) + 1))
            embed = discord.Embed(title="🎵 Song Queued", description=f"Queued: {audio_title}", color=0x00FF00)
            await ctx.send(embed=embed)
        else:
            # Play the requested song
            url, audio_title, pos = queues[guild.id][0] if queues[guild.id] else (url, audio_title, 1)
            audio_source = get_audio_source(url)
            try:
                player = guild.voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(self.on_player_finished(guild, ctx, audio_title), self.bot.loop))
            except discord.errors.ClientException as e:
                print(f"Error: {e}")
            else:
                print("playingidkashdk")
                players[guild.id] = player
                print(player)
                # Update the currently playing song
                self.curr_tracks[guild.id] = (url, audio_title)
                embed = discord.Embed(title="⏯️ Now Playing", description=f"Currently Playing: {audio_title}", color=0x00FF00)
                await ctx.send(embed=embed)
                print(f"Playing audio for {url}")
                # If there are more songs in the queue, load the next one
                if len(queues[guild.id]) > 0:
                    self.bot.loop.create_task(self.load_next_track(guild, ctx))

         
    @music.command()
    async def queue(self, ctx):
        if ctx.guild.id not in queues or len(queues[ctx.guild.id]) == 0:
            embed = discord.Embed(title="❌ Error", description="There are no songs in the queue.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        queue_string = ""
        for i, (url, title, position) in enumerate(queues[ctx.guild.id]):
            queue_string += f"{position}. {title}\n"
        embed = discord.Embed(title="🎵 Queue", description=queue_string, color=0x00FF00)
        await ctx.send(embed=embed)

    @music.command()
    async def idk(self, ctx):
        print(queues)
        print(players)
    
    @music.command()
    async def skip(self, ctx):
        guild = ctx.guild
        # Check if the user is in a voice channel
        if not ctx.author.voice:
            embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Check if the bot is in a voice channel
        if not guild.voice_client:
            embed = discord.Embed(title="❌ Error", description="I am not currently playing any music", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Check if the user is in the same voice channel as the bot
        if ctx.author.voice.channel != guild.voice_client.channel:
            embed = discord.Embed(title="❌ Error", description="You are not in the same voice channel as me", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Check if there are any songs in the queue
        if len(queues[guild.id]) == 0:
            embed = discord.Embed(title="❌ Error", description="There are no songs in the queue", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Check if the guild ID exists in the skip_votes dictionary
        if guild.id not in self.skip_votes:
            self.skip_votes[guild.id] = []
        # Check if the user has already voted to skip the song
        if ctx.author.id in self.skip_votes[guild.id]:
            embed = discord.Embed(title="❌ Error", description="You have already voted to skip this song", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        # Add the user's vote to the skip votes
        self.skip_votes[guild.id].append(ctx.author.id)
        # Check if the number of votes is greater than half the number of members in the voice channel
        if guild.id in self.skip_votes and len(self.skip_votes[guild.id]) >= len(guild.voice_client.channel.members) / 2 and len(guild.voice_client.channel.members) >= 1:
            embed = discord.Embed(title="⏭️ Skip Vote", description=f"{ctx.author.mention} has voted to skip the current song. {len(self.skip_votes[guild.id])}/{round(len(guild.voice_client.channel.members)/2)} votes required to skip the song.", color=0x00FF00)
            self.skip_votes[guild.id] = []
            await ctx.send(embed=embed)
            # Stop playing the current track and load the next track
            if guild.id in queues:
                guild.voice_client.stop()
                # Load the next track in the queue
                await self.load_next_track(guild, ctx)
            else:
                embed = discord.Embed(title="❌ Error", description="I am not currently playing any music", color=0xFF0000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="⏭️ Skip Vote", description=f"{ctx.author.mention} has voted to skip the current song. {len(self.skip_votes[guild.id])}/{round(len(guild.voice_client.channel.members)/2)} votes required to skip the song.", color=0x00FF00)
            await ctx.send(embed=embed)


    # Pause command to pause the audio in the voice channel
    @music.command()
    async def pause(self, ctx):
        guild = ctx.guild
        if not ctx.author.voice:
            embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return
        if guild.voice_client:
            if guild.voice_client.is_playing():
                url, audio_title, pos = queues[guild.id][0]
                audio_title = get_audio_title(url)
                guild.voice_client.pause()
                print(f"{audio_title} paused")
                embed = discord.Embed(
                    title=f"⏯️ {audio_title} has paused",
                    color=0xFFB6C1,
                )
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title=f"🛑 Not currently playing audio",
                    color=0xFFB6C1,
                )
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
            await ctx.response.send_message(embed=embed, ephemeral=True)

    # Resume command to resume the audio in the voice channel
    @music.command()
    async def resume(self, ctx):
        guild = ctx.guild
        if not ctx.author.voice:
            embed = discord.Embed(title="❌ Error", description="You are not connected to a voice channel", color=0xFF0000)
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return
        if guild.voice_client:
            if guild.voice_client.is_paused():
                url, audio_title, pos = queues[guild.id][0]
                audio_title = get_audio_title(url)
                guild.voice_client.resume()
                embed = discord.Embed(
                    title=f"✅ {audio_title}  has resumed",
                    color=0xFFB6C1,
                )
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title=f"🛑 Not currently paused",
                    color=0xFFB6C1,
                )
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="❌ Error", description="The bot is not connected to a voice channel", color=0xFF0000)
            await ctx.response.send_message(embed=embed, ephemeral=True)
    
    @music.command()
    async def stop(self, ctx):
        guild = ctx.guild
        if guild.voice_client:
            if guild.voice_client.is_connected():
                await guild.voice_client.disconnect()
                embed = discord.Embed(
                    title="👋 Leaving",
                    description="I am now leaving the voice channel. Use `/music play` to start playing music again!",
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
            
def setup(bot):
    bot.add_cog(Music(bot))