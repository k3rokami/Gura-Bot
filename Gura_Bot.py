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

from cogs.utility import UtilityMenu
from cogs.genshin import Hoyolab_Cookies,decrypt
from urllib.request import getproxies
from discord.errors import NotFound
from discord.ext import commands, pages, tasks
from discord.ext.pages.pagination import PaginatorButton
from dotenv import load_dotenv
from pysaucenao import SauceNao
from pysaucenao.errors import SauceNaoException
from utils import embeds

VERSION = "v1.2.0"

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
    if current_time == "21:50:50":
        for accounts in Hoyolab_Cookies.keys():
            cookies = Hoyolab_Cookies.get(accounts)
            hashed_ltuid = cookies.get('ltuid')
            hashed_ltoken = cookies.get('ltoken')
            ltuid = decrypt(hashed_ltuid, accounts)
            ltoken = decrypt(hashed_ltoken, accounts)
            user = await bot.fetch_user(accounts)
            channel = await user.create_dm()
            if cookies is None:
                await channel.send(f"Cookies are not set for {user.mention}.Please set cookies with '/set_cookies'",empheral=True)
                return
            # Reuse client instance if it already exists
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
    
if __name__ == '__main__':
    bot.load_extension("cogs.help")
    bot.load_extension("cogs.translator")
    bot.load_extension("cogs.waifu")
    bot.load_extension("cogs.animesearch")
    bot.load_extension("cogs.genshin")
    bot.load_extension("cogs.honkai")
    bot.add_cog(UtilityMenu(bot, VERSION))
        
bot.run(os.environ.get("Discord_Token"), reconnect = True)
