#####################################
# Copyright (c) 2023 Kurokami       #
# Distributed under the MIT License #
#####################################

import asyncio
import datetime
import logging
import os
import typing
import genshin
import discord
import pytz
import subprocess
import platform
import io

from cogs.utility import UtilityMenu
from cogs.genshin import decrypt
from cogs.hoyolab import Hoyolab_Cookies
from urllib.request import getproxies
from discord.errors import NotFound
from discord.ext import commands, pages, tasks
from discord.ext.pages.pagination import PaginatorButton
from dotenv import load_dotenv
from pysaucenao import SauceNao
from pysaucenao.errors import SauceNaoException
from utils import embeds

VERSION = "v1.2.4"

load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
singapore_tz = pytz.timezone("Asia/Singapore")
start_time = datetime.datetime.now(singapore_tz)
Morning_Messages = []
genshin_clients = {}
gura_images=[]

for command in bot.commands:
    bot.remove_command(command.name)
    if isinstance(command, commands.Group):
        for subcommand in command.commands:
            bot.remove_command(subcommand.name)

@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        # synced= await bot.tree.sync()
        # await bot.wait_until_ready()
        # print(f"Synced: {len(synced)} command(s)")
        print(f"Logged in as {bot.user} (ID: {bot.user.id})")
        print(f"Number of slash commands: {len(bot.application_commands)}")
        #send_daily_message.start()
        genshin_daily.start()
        activity = discord.Activity(
            name="Gawr Gura🦈",
            # type=discord.ActivityType.playing,
            type=discord.ActivityType.watching,
        )
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(e)

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title="**======== *Thanks For Adding Me!* ========**",
        description=f"Thanks for adding me to {guild.name}",
        color=0xD89522,
    )
    await guild.text_channels[0].send(embed=embed)

@bot.event
async def on_message(message):
    authorized_users = [671660297102295070, 221916610116583424, 294111764768096266]
    if message.author.bot:
        return
    if message.content.startswith(f'<@{bot.user.id}> sh') or message.content.startswith(f'<@{bot.user.id}>'):
        if message.author.id not in authorized_users:
            embed = discord.Embed(title="Unauthorized Access", description="You are not authorized to run this command.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return
        
        command = message.content[len(f'<@{bot.user.id}> sh'):]

        if platform.system() == "Windows":
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                output, error = proc.communicate()
            except Exception as e:
                output = str(e)
        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable='/bin/bash', universal_newlines=True)
                output, error = proc.communicate()
            except Exception as e:
                output = str(e)

        # split the output into chunks of 1900 characters and send each chunk separately
        for chunk in [output[i:i+1900] for i in range(0, len(output), 1900)]:
            if isinstance(message.channel, discord.DMChannel):
                await message.channel.send(f'```{chunk}```')
                await asyncio.sleep(1)
            elif isinstance(message.channel, discord.GroupChannel):
                await message.channel.send(f'```{chunk}```')
                await asyncio.sleep(1)
            else:
                channel = bot.get_channel(message.channel.id)
                await channel.send(f'```{chunk}```')
                await asyncio.sleep(1)

        if output.startswith('Traceback'):
            embed = discord.Embed(title="Command Error", description=f"```{output}```", color=discord.Color.red())
            channel = bot.get_channel(message.channel.id)
            await channel.send(embed=embed)
    
    if message.content.startswith(f'<@{bot.user.id}> sh logout'):
        embed = discord.Embed(title="Logout:", description=f"Process ID:{proc.pid} has been terminated.", color=discord.Color.blurple())
        channel = bot.get_channel(message.channel.id)
        await channel.send(embed=embed)
        proc.kill()
        return
    
    if message.content.startswith(f'<@{bot.user.id}> up'):
        if message.author.id not in authorized_users:
            embed = discord.Embed(title="Unauthorized Access", description="You are not authorized to run this command.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        if not message.attachments:
            embed = discord.Embed(title="File Upload Error", description="Please attach a file to upload.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        file = message.attachments[0]
        abs_path = message.content.split(' ')[-1]
        file_path = abs_path + file.filename

        try:
            with open(file_path, 'wb') as f:
                await file.save(f)
            embed = discord.Embed(title="File Upload Success", description=f"`{file.filename}` has been uploaded to `{abs_path}`.", color=discord.Color.green())
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="File Upload Error", description=f"An error occurred while uploading `{file.filename}` to `{abs_path}`: `{str(e)}`", color=discord.Color.red())
            await message.channel.send(embed=embed)

    if message.content.startswith(f'<@{bot.user.id}> list'):
        if message.author.id not in authorized_users:
            embed = discord.Embed(title="Unauthorized Access", description="You are not authorized to run this command.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        folder_path = message.content.split(' ')[-1] if len(message.content.split(' ')) > 2 else './'
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        embed = discord.Embed(title="List of Files", description=f"Folder: `{folder_path}`", color=discord.Color.dark_gold())
        
        for file in files:
            embed.add_field(name=file, value=f"Size: `{os.path.getsize(os.path.join(folder_path, file))}` bytes", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith(f'<@{bot.user.id}> get'):
        if message.author.id not in authorized_users:
            embed = discord.Embed(title="Unauthorized Access", description="You are not authorized to run this command.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        file_path = message.content.split(' ')[-1]

        if not os.path.isfile(file_path):
            embed = discord.Embed(title="File Retrieval Error", description=f"`{file_path}` does not exist or is not a file.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return

        with open(file_path, 'rb') as f:
            file_data = io.BytesIO(f.read())
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        embed = discord.Embed(title=f"{file_name} ({file_size} bytes)", color=discord.Color.og_blurple())
        await message.channel.send(embed=embed)
        await message.channel.send(file=discord.File(file_data, file_name))
        
    else:
        ctx = await bot.get_context(message)
        await bot.invoke(ctx)

## Morning Messages
# @tasks.loop(seconds=1)
# async def send_daily_message():
#     now = datetime.datetime.now(singapore_tz)
#     current_time = now.time().strftime("%H:%M:%S")
#     if current_time == "08:30:00":
#         # Iterate through all subscribed users
#         for user_id in Morning_Messages:
#             # Get the user's DM channel
#             user = await bot.fetch_user(user_id)
#             channel = await user.create_dm()
#             # Send the good morning message to the user's DM channel
#             generated_gura_images = random.choice(gura_images)
#             embed = discord.Embed(
#                 title="おはようございます~",
#                 description=f"Good morning, <@{user_id}>! I hope you have a great day today.\n-Gura",
#                 color=0xFFB6C1,
#             )
#             embed.set_image(url=generated_gura_images)
#             await channel.send(embed=embed)
#         # Sleep for 24 hours
#         await asyncio.sleep(24 * 60 * 60)

@tasks.loop(seconds=1)
async def genshin_daily():
    now = datetime.datetime.now(singapore_tz)
    current_time = now.time().strftime("%H:%M:%S")
    if current_time == "10:43:00":
        for accounts in Hoyolab_Cookies.keys():
            cookies = Hoyolab_Cookies.get(accounts)
            if cookies is None:
                await channel.send(f"Cookies are not set for {user.mention}.Please set cookies with '/genshin cookies'",empheral=True)
                return
            hashed_ltuid = cookies.get('ltuid')
            hashed_ltoken = cookies.get('ltoken')
            ltuid = decrypt(hashed_ltuid, accounts)
            ltoken = decrypt(hashed_ltoken, accounts)
            user = await bot.fetch_user(accounts)
            channel = await user.create_dm()
            if accounts in genshin_clients:
                client = genshin_clients[accounts]
            else:
                client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},game=genshin.Game.GENSHIN)
                genshin_clients[accounts] = client
            try:
                reward = await client.claim_daily_reward()
            except genshin.AlreadyClaimed:
                # print("Daily reward already claimed")
                signed_in, claimed_rewards = await client.get_reward_info()
                embed = discord.Embed(
                    title="Genshin Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                embed.add_field(name="Reward:", value="Daily reward already claimed",inline=False)
                embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
                embed.set_footer(
                    text=f"Requested by {user.mention}",
                    icon_url=user.display_avatar,
                )
                await channel.send(embed=embed, delete_after=1800)
                # print(f"Signed in: {signed_in} | Total claimed rewards this month: {claimed_rewards}")
            except Exception as e:
                if not genshin.AccountNotFound:
                    claimed_rewards = await client.get_reward_info()
                    embed = discord.Embed(
                        title="Genshin Hoyolab Daily Check-In",
                        color=0xFFB6C1,
                    )
                    embed.add_field(name="An error has occured:", value=f"{e}",inline=False)
                    embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
                    embed.set_footer(
                        text=f"Requested by {user.mention}",
                        icon_url=user.display_avatar,
                    )
                    await channel.send(embed=embed, delete_after=1800)
                else:
                    embed = discord.Embed(
                        title="Genshin Hoyolab Daily Check-In",
                        color=0xFFB6C1,
                    )
                    embed.add_field(name="An error has occured:", value=f"{e}",inline=False)
                    embed.set_footer(
                        text=f"Requested by {user.mention}",
                        icon_url=user.display_avatar,
                    )
                    await channel.send(embed=embed, delete_after=1800)
            else:
                # print(f"Claimed {reward.amount}x {reward.name}")
                signed_in, claimed_rewards = await client.get_reward_info()
                embed = discord.Embed(
                    title="Genshin Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                embed.add_field(name="Reward:", value=f"{reward.amount}x {reward.name}",inline=False)
                embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
                embed.set_footer(
                    text=f"Requested by {user.mention}",
                    icon_url=user.display_avatar,
                )
                await channel.send(embed=embed, delete_after=1800)
        # Sleep for 24 hours
        await asyncio.sleep(24 * 60 * 60)

@bot.slash_command(name="hello", description="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hey{interaction.user.mention}! This is a bot built by **Kurokami**",
        ephemeral=True,
    )

# Main Function

# @bot.slash_command(
#     name="subscribe", description="Gura sends you a morning message every morning"
# )
# async def subscribe(interaction: discord.Interaction):
#     # Add the user to the subscribed users dictionary
#     try:
#         if interaction.user.id not in Morning_Messages:
#             Morning_Messages.append(interaction.user.id)
#             print(Morning_Messages)
#             await interaction.response.send_message(
#                 f"{interaction.user.mention}, you are now subscribed to the daily morning messages!"
#             )
#         else:
#             await interaction.response.send_message(
#                 f"{interaction.user.mention}, you are already subscribed to the daily morning messages!"
#             )
#     except:
#         await interaction.response.send_message(
#             f"Occured an error adding {interaction.user.mention}"
#         )


# @bot.slash_command(
#     name="unsubscribe", description="Gura stops sending you morning messages"
# )
# async def unsubscribe(interaction: discord.Interaction):
#     try:
#         if interaction.user.id in Morning_Messages:
#             Morning_Messages.remove(interaction.user.id)
#             print(interaction.user.id)
#             await interaction.response.send_message(
#                 f"{interaction.user.mention}, you are removed from daily good morning messages!"
#             )
#         else:
#             await interaction.response.send_message(
#                 f"{interaction.user.mention}, you are not subscribed to it! `/subscribe` to recieve daily morning messages."
#             )
#     except:
#         await interaction.response.send_message(
#             f"Occured an error removing {interaction.user.mention}"
#         )


# SauceNao Stuff
log = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s"
)

try:
    sauce = SauceNao(
        api_key=str(os.environ.get("SauceNao_API")),
        results_limit=int(os.environ.get("SauceNao_ResultLimit")),
        min_similarity=float(os.environ.get("SauceNao_MinSimilarity")),
        proxy=getproxies(),
    )
except Exception as e:
    log.error(f"Failed to initialize SauceNao object: {e}")

@bot.command(name="saucenao", aliases=["source", "sauce", "sause", "nao", "search"])
async def saucenao(ctx, src: typing.Optional[str]):
    resultsPages = []
    results = None
    try:
        if src:
            if src.startswith("<@"):
                try:
                    member = await bot.fetch_user(src.strip("<@!>"))
                except NotFound:
                    await ctx.send(
                        embed=embeds.error_embed(
                            title="Not Found!",
                            description="The user mentioned does not exist.",
                        )
                    )
                    return
                results = await sauce.from_url(member.avatar.url)
            elif src.isdigit():
                try:
                    member = await bot.fetch_user(src)
                except NotFound:
                    await ctx.send(
                        embed=embeds.error_embed(
                            title="Not Found!",
                            description="The user ID given does not belong to any user.",
                        )
                    )
                    return
                results = await sauce.from_url(member.avatar.url)
            elif src.startswith("https://") or src.startswith("http://"):
                results = await sauce.from_url(src)
            else:
                await ctx.send(
                    embed=embeds.error_embed(
                        title="Not a URL!",
                        description="The argument given is not a URL.",
                    )
                )
                return
        else:
            if ctx.message.attachments:
                results = await sauce.from_url(ctx.message.attachments[0].url)
            else:
                await ctx.send(embed=embeds.help_embed())
                return
        try:
            if results is None:
                raise IndexError
            for result in results:
                resultsPages.append(
                    embeds.results_embed(
                        database=f"[{result.index}]({result.url})",
                        similarity=result.similarity,
                        author=f"[{result.author_name}]({result.author_url})",
                        title=result.title,
                        thumbnail=result.thumbnail,
                    ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
                )
            if len(results) > 1:
                paginator = pages.Paginator(
                    pages=resultsPages,
                    show_disabled=False,
                    show_indicator=True,
                    author_check=False,
                )
                paginator.add_button(
                    PaginatorButton(
                        button_type="prev", emoji="⬅️", style=discord.ButtonStyle.grey
                    )
                )
                paginator.add_button(
                    PaginatorButton(
                        button_type="next", emoji="➡️", style=discord.ButtonStyle.grey
                    )
                )
                paginator.add_button(
                    PaginatorButton(
                        button_type="first", emoji="⏪", style=discord.ButtonStyle.grey
                    )
                )
                paginator.add_button(
                    PaginatorButton(
                        button_type="last", emoji="⏩", style=discord.ButtonStyle.grey
                    )
                )
                await paginator.send(ctx)
            else:
                await ctx.send(embed=resultsPages[0])
        except IndexError:
            await ctx.send(
                embed=embeds.error_embed(
                    title="No Results!",
                    description="""
                    Gura can't find the source of the image. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locator websites like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe).
                    """,
                ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
            )
    except SauceNaoException as e:
        await ctx.send(
            embed=embeds.error_embed(
                title="API Error!",
                description=f"""
                Failed to get results from the image.\n\n**Error:** {e}
                """,
            )
        )


# Using Application Command
@bot.message_command(name="Get Image Source")
async def saucenao(ctx: commands.Context, message: discord.Message):
    resultsPages = []
    results = None
    if message.embeds:
        for embed in message.embeds:
            if embed.thumbnail and embed.thumbnail.url:
                # Use the thumbnail image URL
                results = await sauce.from_url(str(embed.thumbnail.url))
            elif embed.image and embed.image.url:
                # Use the image URL
                results = await sauce.from_url(str(embed.image.url))
    elif message.attachments:
        for attachment in message.attachments:
            results = await sauce.from_url(str(attachment.url))
    else:
        await ctx.respond(
            embed=embeds.error_embed(
                title="Not an Image or an Embed Image!",
                description="The given is not an Image or an Embed Image.\n**Please use !sauce**",
            ),
            ephemeral=True,
        )
        return

    try:
        if results is None:
            raise IndexError
        for result in results:
            resultsPages.append(
                embeds.results_embed(
                    database=f"[{result.index}]({result.url})",
                    similarity=result.similarity,
                    author=f"[{result.author_name}]({result.author_url})",
                    title=result.title,
                    thumbnail=result.thumbnail,
                ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
            )
        if len(results) > 1:
            message = await ctx.send(embed=resultsPages[0])
            if ctx.guild:  # If used in a group
                i = 0
                await message.add_reaction("⬅️")
                await message.add_reaction("➡️")
                await message.add_reaction("✅")
                while True:
                    try:
                        reaction, user = await bot.wait_for(
                            "reaction_add",
                            timeout=60.0,  # 60 seconds timeout
                            check=lambda r, u: str(r.emoji) in ["⬅️", "➡️", "✅"]
                            and r.message.id == message.id,
                        )
                        if str(reaction.emoji) == "➡️" and i < len(resultsPages) - 1:
                            i += 1
                            await message.edit(embed=resultsPages[i])
                            await message.remove_reaction("➡️", user)
                        elif str(reaction.emoji) == "⬅️" and i > 0:
                            i -= 1
                            await message.edit(embed=resultsPages[i])
                            await message.remove_reaction("⬅️", user)
                        elif str(reaction.emoji) == "✅":
                            await message.clear_reactions()
                            break
                        await reaction.remove(user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
        else:
            await ctx.send(embed=resultsPages[0])
    except IndexError:
        await ctx.send(
            embed=embeds.error_embed(
                title="No Results!",
                description="""
                Gura can't find the source of the image. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locator websites like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe).
                """,
            ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
        )
    except SauceNaoException as e:
        await ctx.send(
            embed=embeds.error_embed(
                title="API Error!",
                description=f"Failed to get results from the image.\n\n**Error:** {e}",
            )
        )

# Using User Command
@bot.user_command(name="Search Avatar Source")
async def saucenao(ctx: commands.Context, member: discord.Member):
    resultsPages = []
    results = None
    if member.avatar:
        results = await sauce.from_url(str(member.avatar.url))
    else:
        await ctx.respond(
            embed=embeds.error_embed(
                title="Not a User!",
                description="The given is not a User.\n**Please use !sauce**",
            ),
            ephemeral=True,
        )
        return

    try:
        if results is None:
            raise IndexError
        for result in results:
            resultsPages.append(
                embeds.results_embed(
                    database=f"[{result.index}]({result.url})",
                    similarity=result.similarity,
                    author=f"[{result.author_name}]({result.author_url})",
                    title=result.title,
                    thumbnail=result.thumbnail,
                ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
            )
        if len(results) > 1:
            message = await ctx.send(embed=resultsPages[0])
            if ctx.guild:  # If used in a group
                i = 0
                await message.add_reaction("⬅️")
                await message.add_reaction("➡️")
                await message.add_reaction("✅")
                while True:
                    try:
                        reaction, user = await bot.wait_for(
                            "reaction_add",
                            timeout=60.0,  # 60 seconds timeout
                            check=lambda r, u: str(r.emoji) in ["⬅️", "➡️", "✅"]
                            and r.message.id == message.id,
                        )
                        if str(reaction.emoji) == "➡️" and i < len(resultsPages) - 1:
                            i += 1
                            await message.edit(embed=resultsPages[i])
                            await message.remove_reaction("➡️", user)
                        elif str(reaction.emoji) == "⬅️" and i > 0:
                            i -= 1
                            await message.edit(embed=resultsPages[i])
                            await message.remove_reaction("⬅️", user)
                        elif str(reaction.emoji) == "✅":
                            await message.clear_reactions()
                            break
                        await reaction.remove(user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
        else:
            await ctx.send(embed=resultsPages[0])
    except IndexError:
        await ctx.send(
            embed=embeds.error_embed(
                title="No Results!",
                description="""
                Gura can't find the source of the image. Maybe the results had low similarity percentage?\n\nPlease use other ways of finding the source either by reverse image searching or using source locator websites like [SauceNao](https://saucenao.com/) and [trace.moe](https://trace.moe).
                """,
            ).set_footer(text=f"{results.long_remaining}/{results.long_limit}")
        )
    except SauceNaoException as e:
        await ctx.send(
            embed=embeds.error_embed(
                title="API Error!",
                description=f"Failed to get results from the image.\n\n**Error:** {e}",
            )
        )
        
# @bot.slash_command(name="unload", description="Unload a specific cog")
# async def unload_cog(ctx, cog_name: str):
#     try:
#         bot.unload_extension(f"cogs.{cog_name}")
#         await ctx.send(f"Successfully unloaded the {cog_name} cog!")
#     except Exception as e:
#         await ctx.send(f"An error occurred while unloading the {cog_name} cog: {str(e)}")
            
# @bot.slash_command(name="reload", description="Reload cog")
# async def reload_cog(ctx, cog_name):
#     try:
#         bot.reload_extension(cog_name)
#         cog = bot.get_cog(cog_name)
#         cog.cog_reload()
#         await ctx.send(f"Successfully reloaded the {cog_name} cog and updated slash commands!")
#     except Exception as e:
#         await ctx.send(f"An error occurred while reloading the {cog_name} cog: {str(e)}")
        
# @bot.slash_command(name="load", description="Load a specific cog")
# async def reload_cog(ctx, cog_name: str):
#     try:
#         bot.load_extension(f"cogs.{cog_name}")
#         await ctx.send(f"Successfully loaded the {cog_name} cog!")
#     except Exception as e:
#         await ctx.send(f"An error occurred while loading the {cog_name} cog: {str(e)}")
        
if __name__ == '__main__':
    cog_list = ['cogs.help', 'cogs.translator', 'cogs.waifu', 'cogs.animesearch', 'cogs.genshin', 'cogs.honkai']
    for cog in cog_list:
        bot.load_extension(cog)
    bot.add_cog(UtilityMenu(bot, VERSION))
        
bot.run(os.environ.get("Discord_Token"), reconnect = True)
