import discord,os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Client, Intents, Embed
from discord.ext.commands.core import command
import DiscordUtils
import ffmpeg

load_dotenv()
music = DiscordUtils.Music()
activity = discord.Game(name="around. Use /help")
bot = commands.Bot(command_prefix='!')

@bot.slash_command()
async def join(ctx):
    voicetrue = ctx.author.voice
    if voicetrue is None:
        return await ctx.send('You are not currently in a voice channel. :exclamation:')
    await ctx.author.voice.channel.connect()
    await ctx.send('Joined the voice chat you are in. :white_check_mark:')

@bot.slash_command()
async def leave(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send('You are not currently in the same voice channel as I am.')
    if mevoicetrue is None:
        return await ctx.send('Im not currently in any voice channel!')
    await ctx.voice_client.disconnect()
    await ctx.send('I have disconnected from the voice channel.')

@bot.slash_command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_bettercix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f'Playing **{song.name}** :notes:')
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f'Ive added **{song.name}** to the queue!')

@bot.slash_command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"The music queue currently is: **{', '.join([song.name for song in player.current_queue()])}**")

@bot.slash_command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f'Paused **{song.name}** :pause_button:')

@bot.slash_command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f'Resumed **{song.name}** :arrow_forward:')

@bot.slash_command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f'{song.name} will now start looping. :repeat:')
    else:
        return await ctx.send(f'{song.name} will no longer loop. :no_entry:')

@bot.slash_command()
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    if song.name is None:
        await ctx.send(song.name + ' is currently playing.')

@bot.slash_command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue
    await ctx.send(f'Removed {song.name} from the song queue!')
    

@bot.slash_command(
    name="hello",
    description="Hello there!",
    guild_ids=[822512275331219517, 708384142978711582, 747869167889285180]
)
async def _hello(ctx):
    await ctx.send("Hi! test command")

@bot.slash_command(
    name="help",
    description="Recieve help using Anix",
    guild_ids=[822512275331219517, 708384142978711582, 747869167889285180]
)
async def _help(ctx):
    embed=discord.Embed(title="Commands to get you going", description="", color=0xff131a)
    embed.set_author(name="Anix Help")
    embed.add_field(name="?play", value="use this command whilst in a voice channel to start music", inline=False)
    embed.add_field(name="?join", value="make Anix join your voice channel", inline=False)
    embed.add_field(name="?leave", value="make Anix leave your voice channel", inline=False)
    embed.add_field(name="?queue", value="check the music queue", inline=False)
    embed.add_field(name="?pause", value="pauses the current song that's playing", inline=False)
    embed.add_field(name="?resume", value="resumes a paused song", inline=False)
    embed.add_field(name="?loop", value="loops the current song (type again to stop loop)", inline=False)
    embed.add_field(name="?nowplaying", value="check the song that's currently playing", inline=True)
    embed.add_field(name="?remove", value="removes the currently playing song from the queue", inline=True)
    await ctx.send(embeds=[embed])
    
bot.run(os.getenv('DISCORD_TOKEN'))