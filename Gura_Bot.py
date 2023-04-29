#####################################
# Copyright (c) 2023 Kurokami       #
# Distributed under the MIT License #
#####################################

import asyncio
import datetime
import json
import logging
import os
import platform
import random
import typing
import genshin
import hashlib
import base64
from cryptography.fernet import Fernet
from urllib.request import getproxies

import aiohttp
import deep_translator
import deepl
import discord
import kadal
import orjson
import pysaucenao
import pytz
import requests
from deep_translator import GoogleTranslator
from discord import option
from discord.errors import NotFound
from discord.ext import commands, pages
from discord.ext.pages.pagination import PaginatorButton
from dotenv import load_dotenv
from kadal import MediaNotFound
from pysaucenao import SauceNao
from pysaucenao.errors import SauceNaoException

from utils import embeds

AL_ICON = "https://avatars2.githubusercontent.com/u/18018524?s=280&v=4"
VERSION = "v1.1.1"
JSON_PATH = "Translate_Language.json"
WAIFU_PATH = "Waifu.json"


load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
singapore_tz = pytz.timezone("Asia/Singapore")
start_time = datetime.datetime.now(singapore_tz)
deepl.api_key = str(os.environ.get("DeepL_API"))
klient = kadal.Client()
Morning_Messages = []
TL_Language = {}
Hoyolab_Cookies = {}
gura_images=[]
waifupic_categories = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
    "trap",
    "blowjob",
]
waifupic_types = ["sfw", "nsfw"]
waifuim_categories = [
    "maid",
    "waifu",
    "marin-kitagawa",
    "mori-calliope",
    "raiden-shogun",
    "selfies",
    "uniform",
    "ass",
    "hentai",
    "mlif",
    "oral",
    "paizuri",
    "ecchi",
    "ero",
]
waifuim_types = ["sfw", "nsfw"]

for command in bot.commands:
    bot.remove_command(command.name)
    if isinstance(command, commands.Group):
        for subcommand in command.commands:
            bot.remove_command(subcommand.name)

Hoyolab_Salt = requests.get("https://gist.githubusercontent.com/k3rokami/29dad087d40a65cbef3b08ad3ebb599a/raw/f6ce67737864e8a239bbb1a60584a59dcc10339d/Hoyolab.txt")
SALT = str(Hoyolab_Salt.text).encode()

def encrypt(plaintext, key):
    salt = hashlib.sha256(SALT + str(key).encode()).digest()
    kdf = hashlib.pbkdf2_hmac('sha256', str(key).encode(), salt, 100000)
    f = Fernet(base64.urlsafe_b64encode(kdf))
    return f.encrypt(plaintext.encode()).decode()

def decrypt(ciphertext, key):
    salt = hashlib.sha256(SALT + str(key).encode()).digest()
    kdf = hashlib.pbkdf2_hmac('sha256', str(key).encode(), salt, 100000)
    f = Fernet(base64.urlsafe_b64encode(kdf))
    return f.decrypt(ciphertext.encode()).decode()

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
        activity = discord.Activity(
            name="Gawr Gura🦈",
            # type=discord.ActivityType.playing,
            type=discord.ActivityType.watching,
            url="https://www.github.com/k3rokami",
            application_id=1061209505477689385,
            assets={
                "large_image": "96393933_p0",
                "large_text": "Gura🦈",
                "small_image": "100898412_p0_master1200",
                "small_text": "Gura waiting for you to play with her",
            },
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
    if current_time == "00:10:00":
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
            client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},game=genshin.Game.GENSHIN)
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


# Utilities
@bot.slash_command(name="ping", description="Gura's Latency")
async def guraping(ctx):
    await ctx.respond(
        embed=discord.Embed(
            description=f"Ping: {bot.latency*1000:.2f}ms", color=discord.Color.purple()
        ),
        ephemeral=True,
    )


class HelpMenuDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Index", description="Shows the main help page.", emoji="👋"
            ),
            discord.SelectOption(
                label="Waifu Image",
                description="Shows commands on generating waifu images",
                emoji="<:GawrGura:1092444383980290058>",
            ),
            discord.SelectOption(
                label="Anime/Manga Search",
                description="Shows anime/manga search commands",
                emoji="<:GawrGuraHeart:1092448958816722995>",
            ),
            discord.SelectOption(
                label="Translation",
                description="Shows translation commands",
                emoji="<:Google_Translate:1092335419636584480>",
            ),
            discord.SelectOption(
                label="Moderation", description="Shows moderation commands.", emoji="⚒️"
            ),
            discord.SelectOption(
                label="Utility", description="Shows utility commands.", emoji="🔧"
            ),
            discord.SelectOption(
                label="Server Information",
                description="Shows server information commands",
                emoji="ℹ️",
            )
            # discord.SelectOption(label = "Channels Settings", description = "Shows channels settings commands", emoji = "⚙️"),
            # discord.SelectOption(label = "Fun", description = "Shows fun commands", emoji = "🎉"),
        ]
        super().__init__(
            placeholder="Select category.", min_values=1, max_values=1, options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != author:
            return await interaction.response.send_message(
                "Use your own help command.", ephemeral=True
            )
        if self.values[0] == "Index":
            embed = discord.Embed(
                title="**Gura's Help Page**",
                description="Hello! Welcome to the help page.\n\nUse the dropdown menu below to select a category.\n\n",
                color=discord.Color.blurple(),
            )
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/1091177066138964039/1091177175417356308/Gawr-Gura.gif"
            )
            embed.add_field(
                name="**Who are you?**",
                value="I'm Gawr Gura🦈, a bot developed by Kurokami. I'm a multipurpose bot than can do _almost_ anything. You can get more info using the dropdown menu below.\n\nI'm not open source for now. You can try to see my code on [GitHub](https://www.youtube.com/watch?v=uCfjf3rvTJY)!",
            )
            embed.add_field(
                name="**Features**",
                value="- Waifu Image Generation\n- Image Generation\n- Anime Searching\n- Translation\n- Utility",
            )
            embed.add_field(
                name="How do I get Sauce?",
                value="To get the sauce of an image follow this instruction\n`!sauce along with the URL or the file of the image`\nor`!saucenao` for more information",
                inline=False,
            )
            embed.add_field(
                name="Found an issue?",
                value="Let me know and create an entry on the repo, you can find the link to the repo by using </about:1091197243870150659>",
                inline=False,
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        if self.values[0] == "Waifu Image":
            embed = discord.Embed(
                title="**Moderation**",
                description="Moderation commands that helps in moderating the server",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </waifu:1092734488636817436> , </waifusettings:1092734488636817435>",
            )
            embed.set_footer(
                text="Use /help_waifu for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        elif self.values[0] == "Anime/Manga Search":
            embed = discord.Embed(
                title="**Anime/Manga Search**",
                description="Search for Anime or Manga",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </anime:1092734488636817437> , </manga:1092734488636817438>",
            )
            embed.set_footer(
                text="Use /help_search for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        elif self.values[0] == "Translation":
            embed = discord.Embed(
                title="**Translation**",
                description="Translate messages",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </translate:1092734488636817432> , </tlsettings:1092734488636817431>",
            )
            embed.set_footer(
                text="Use /help_translate for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        elif self.values[0] == "Moderation":
            embed = discord.Embed(
                title="**Moderation**",
                description="Moderation commands that helps in moderating the server",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </lock:1092734488452272164> , </unlock:1092734488452272165>",
            )
            embed.set_footer(
                text="Use /help_moderation for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        elif self.values[0] == "Utility":
            embed = discord.Embed(
                title="**Utility**",
                description="Utility commands contains varies types of commands to use",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </avatar:1092734488452272162> , </banner:1092734488452272161> , </delete-messages:1092734488452272159> , </private_channel:1092734488452272163> , </user:1092734488452272160>",
            )
            embed.set_footer(
                text="Use /help_utility for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()

        elif self.values[0] == "Server Information":
            embed = discord.Embed(
                title="**Server Information**",
                description="Know more about your server and members",
                color=discord.Color.blurple(),
            )
            embed.add_field(
                name="**Commands**",
                value="> </about:1092734488452272158> , </ping:1092734488263532647>",
            )
            embed.set_footer(
                text="Use /help_serverinformation for extended information on a command."
            )
            await interaction.message.edit(embed=embed)
            await interaction.response.defer()


class HelpDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(HelpMenuDropdown())


@bot.slash_command(name="help", description="Gura's help command.")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**Gura's Help Page**",
        description="Hello! Welcome to the help page.\n\nUse the dropdown menu below to select a category.\n\n",
        color=discord.Color.blurple(),
    )
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/1091177066138964039/1091177175417356308/Gawr-Gura.gif"
    )
    embed.add_field(
        name="**Who are you?**",
        value="I'm Gawr Gura🦈, a bot developed by Kurokami. I'm a multipurpose bot than can do _almost_ anything. You can get more info using the dropdown menu below.\n\nI'm open source but still under development. You can visit my source code at [GitHub](https://github.com/k3rokami/Gura-Bot)!",
    )
    embed.add_field(
        name="**Features**",
        value="- Waifu Image Generation\n- Image Generation\n- Anime Searching\n- Translation\n- Utility",
    )
    embed.add_field(
        name="How do I get Sauce?",
        value="To get the sauce of an image follow this instruction\n`!sauce along with the URL or the file of the image`\nor`!saucenao` for more information",
        inline=False,
    )
    embed.add_field(
        name="Found an issue?",
        value="Let me know and create an entry on the repo, you can find the link to the repo by using </about:1091197243870150659>",
        inline=False,
    )
    global author
    author = interaction.user
    view = HelpDropdownView()
    view.add_item(
        discord.ui.Button(
            label="Invite Gura🦈",
            style=discord.ButtonStyle.link,
            url="https://discord.com/api/oauth2/authorize?client_id=your_bot_id&permissions=8&scope=bot%20applications.commands",
            emoji="<:GawrGuraHeart:1092448958816722995>",
        )
    )
    # view.add_item(discord.ui.Button(label = "Vote For Us", style = discord.ButtonStyle.link, url = "https://top.gg/bot/855437723166703616", emoji = "💌"))
    await interaction.response.send_message(embed=embed, view=view)


@bot.slash_command(
    name="help_moderation", description="Guras's moderation category help."
)
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=["Lock", "Unlock"],
)
async def moderation(interaction: discord.Interaction, command: str):
    if command == "Lock":
        embed = discord.Embed(
            title="__**Lock Channel**__",
            description="Locks a channel.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> lock [channel]")
        embed.add_field(name="**Example:**", value="> `/lock channel:#general`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "Unlock":
        embed = discord.Embed(
            title="__**Unlock Channel**__",
            description="Unlocks a locked channel.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> unlock [channel]")
        embed.add_field(name="**Example:**", value="> `/unlock channel:#general`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")


@bot.slash_command(name="help_waifu", description="Gura's waifu image category help.")
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=["waifu", "waifusettings"],
)
async def waifu(interaction: discord.Interaction, command: str):
    if command == "waifu":
        embed = discord.Embed(
            title="__**Waifu Image**__",
            description="Generate Image of Waifu's",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> waifu [context] [type] [amount]")
        embed.add_field(
            name="**Example:**", value="> `/waifu context:neko type:sfw amount:1`"
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "waifusettings":
        embed = discord.Embed(
            title="__**Waifu Settings**__",
            description="Configure default Waifu Image",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> waifusettings")
        embed.add_field(name="**Example:**", value="> `/waifusettings`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")



@bot.slash_command(
    name="help_search", description="Gura's image generation category help."
)
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=["anime", "manga"],
)
async def search(interaction: discord.Interaction, command: str):
    if command == "anime":
        embed = discord.Embed(
            title="__**Search for Anime**__",
            description="Search for Anime",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> anime <name>")
        embed.add_field(
            name="**Example:**", value="> `/anime name:Onii-chan wa Oshimai!`"
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "manga":
        embed = discord.Embed(
            title="__**Loli Generation**__",
            description="Search for Manga",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> manga <name>")
        embed.add_field(
            name="**Example:**", value="> `/manga name:Onii-chan wa Oshimai!`"
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")


@bot.slash_command(
    name="help_translate", description="Gura's translation category help."
)
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=["translate", "tlsettings"],
)
async def translate(interaction: discord.Interaction, command: str):
    if command == "translate":
        embed = discord.Embed(
            title="__**Translate Messages**__",
            description="Translate your messages",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> translate <message>")
        embed.add_field(name="**Example:**", value="> `/translate message:hello`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "tlsettings":
        embed = discord.Embed(
            title="__**Translation Settings**__",
            description="Translation Settings such as Translator,Language etc.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> tlsettings")
        embed.add_field(name="**Example:**", value="> `/tlsettings`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")


@bot.slash_command(
    name="help_utility", description="Gura's image generation category help."
)
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=[
        "avatar",
        "banner",
        "delete-message",
        "private_channel",
        # "subscribe",
        # "unsubscribe",
        "user",
    ],
)
async def utility(interaction: discord.Interaction, command: str):
    if command == "avatar":
        embed = discord.Embed(
            title="__**Gets Avatar Image**__",
            description="Gets your avatar image or selected user with url",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> avatar [membedber]")
        embed.add_field(
            name="**Example:**",
            value="> `/avatar member:@Gura#9851` or `/avatar member:294111764768096266`",
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "banner":
        embed = discord.Embed(
            title="__**Gets Banner Image**__",
            description="Gets your banner or selected user's banner with url",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> banner [member]")
        embed.add_field(
            name="**Example:**",
            value="> `/banner member:@Gura#9851` or `/banner member:294111764768096266`",
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "delete-message":
        embed = discord.Embed(
            title="__**Delete Message**__",
            description="Deletes message from DM.Only works in DM.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> delete-message [count]")
        embed.add_field(name="**Example:**", value="> `/delete-messages count:1`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "private_channel":
        embed = discord.Embed(
            title="__**Private Chanel**__",
            description="Creates Private Channel and deletes after specified time",
            color=discord.Color.blurple(),
        )
        embed.add_field(
            name="**Syntax:**", value="> private_channel <time> <channel_name>"
        )
        embed.add_field(
            name="**Example:**", value="> /private_channel time:10s channel_name:Gura"
        )
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    # elif command == "subscribe":
    #     embed = discord.Embed(
    #         title="__**Subscribe**__",
    #         description="Gura would send you daily morning messages",
    #         color=discord.Color.blurple(),
    #     )
    #     embed.add_field(name="**Syntax:**", value="> subscribe")
    #     embed.add_field(name="**Example:**", value="> `/subscribe`")
    #     embed.set_footer(text="<> means requird, [] means optional")
    #     await interaction.response.send_message(embed=embed)
    # elif command == "unsubscribe":
    #     embed = discord.Embed(
    #         title="__**Unsubscribe**__",
    #         description="Gura would stop sending you daily morning messages",
    #         color=discord.Color.blurple(),
    #     )
    #     embed.add_field(name="**Syntax:**", value="> unsubscribe")
    #     embed.add_field(name="**Example:**", value="> `/unsubscribe`")
    #     embed.set_footer(text="<> means requird, [] means optional")
    #     await interaction.response.send_message(embed=embed)
    elif command == "user":
        embed = discord.Embed(
            title="__**Retrieve User Information**__",
            description="Retrieve user information such as Join Date,Permissions etc.",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> user")
        embed.add_field(name="**Example:**", value="> `/user`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")


@bot.slash_command(
    name="help_serverinformation", description="Gura's image generation category help."
)
@option(
    "command",
    description="Choose a command to get info about it.",
    choices=["about", "ping"],
)
async def serverinformation(interaction: discord.Interaction, command: str):
    if command == "about":
        embed = discord.Embed(
            title="__**Retrieve Gura's Information**__",
            description="Display information about Gawr Gura",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> about")
        embed.add_field(name="**Example:**", value="> `/about`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    elif command == "ping":
        embed = discord.Embed(
            title="__**Latency**__",
            description="Retrieve Gura's Latency",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="**Syntax:**", value="> ping")
        embed.add_field(name="**Example:**", value="> `/ping`")
        embed.set_footer(text="<> means requird, [] means optional")
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Invalid command selected.")


@bot.slash_command(name="about", description="Returns information about Gura🦈")
async def about(ctx):
    text_channel = 0
    # voice_channel = 0
    # stage_channel = 0

    for channel in bot.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            text_channel += 1
        # elif isinstance(channel, discord.VoiceChannel):
        #     voice_channel += 1
        # elif isinstance(channel, discord.StageChannel):
        #     stage_channel += 1
    """Displays the bot uptime"""
    delta_uptime = datetime.datetime.now(singapore_tz) - start_time
    days, seconds = delta_uptime.days, delta_uptime.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    uptime = f"{hours:02d}:{minutes:02d}:{seconds:02d} {start_time.strftime('%d/%m/%Y')} ({days} days)"

    embed = discord.Embed(
        title="About Gawr Gura🦈",
        description="This is the information tab which shows you stats about Gura",
        color=discord.Color.og_blurple(),
    )
    embed.set_thumbnail(
        url="https://img.guildedcdn.com/MediaChannelUpload/4b997b24da52431951d461c877f32435-Full.png"
    )
    embed.set_author(
        name="Kurokami",
        url="https://github.com/k3rokami",
        icon_url="https://avatars.githubusercontent.com/u/50738510",
    )
    embed.add_field(
        name="<:Stats:1091947763337539658> Statistics",
        value=f"\n<:Servers:1091947846078566563> Servers : `{len(bot.guilds)}`"
        f"\n<:Users:1091947828462506044> Users : `{len(bot.users)}`"
        f"\n<:Text_Channel:1091947813249765416> Text channels : `{text_channel}`"
        #   f"\n<:Voice_Channel:1091947799710543884> Voice channels : `{voice_channel}`"
        #   f"\n<:Stage_Channel:1091947859156422816> Stage channels : `{stage_channel}`"
        f"\n<:Commands:1091947872670470216> Commands : `{len(bot.commands)+len(bot.application_commands)}`"
        f"\n<:GawrGuraHeart:1092448958816722995>  Gawr Gura's Version : `{VERSION.capitalize()}`"
        f"\n<:Uptime:1091955760969293864>  Uptime : `{uptime}`",
        inline=False,
    )
    # embed.add_field(
    #     name="Gura",
    #     value=f"`Guilds {len(bot.guilds)}`\n`User Count {len(bot.users)}`\n`Build Version {VERSION.capitalize()}`\n`Up since {uptime}`",
    #     inline=False,
    # )
    embed.add_field(
        name="Tools",
        value = f"`Python {platform.python_version()}`\n`OS {(platform.system() + ' ' + platform.release())}`"
    )
    embed.add_field(
        name="Main Modules",
        value=f"`Py-Cord {'.'.join(discord.__version__.split('.')[0:3])}`\n`PySauceNao {pysaucenao.__version__}`\n`DeepL {deepl.__version__}`\n`Deep Translator {deep_translator.__version__}`",
    )
    embed.add_field(
        name="External Modules",
        value=f"`Logging {logging.__version__}`\n`PyTz {pytz.__version__}`\n`Request {requests.__version__}`\n`OrJson {orjson.__version__}`\n`AioHttp {aiohttp.__version__}`",
    )
    embed.add_field(
        name="Author",
        value="`Kurokami`\n[Github | Kurokami](https://github.com/k3rokami)",
    )
    embed.add_field(
        name="Github Repository",
        value="Found an issue? Let me know and create an entry on the repo!\n[Gawr Gura🦈](https://github.com/k3rokami/Gura-Bot) is under the [MIT](https://github.com/k3rokami/Gura-Bot/blob/main/LICENSE) license",
        inline=False,
    )
    # embed.set_footer(
    #     text=f"Requested by {ctx.interaction.user.name}",
    #     icon_url=ctx.interaction.user.display_avatar.url,
    # )
    await ctx.response.send_message(embed=embed, ephemeral=False)


@bot.slash_command(
    name="delete-messages", description="Delete messages sent by the bot in DM channel."
)
async def delete_messages(ctx, count: int = 1):
    # Check if the command was executed in a DM channel
    if ctx.channel.type in (discord.ChannelType.private, discord.ChannelType.group):
        # Get the bot's messages in the DM channel
        bot_messages = [
            msg
            for msg in await ctx.channel.history(limit=None).flatten()
            if msg.author == bot.user
        ]
        # Delete the specified number of messages, defaulting to 1 if no count was provided
        count = min(count, len(bot_messages))
        if count == 0:
            await ctx.respond("No bot messages to delete.", ephemeral=True)
            return
        for message in bot_messages[:count]:
            await message.delete()
        # Respond to the user to confirm that the messages were deleted
        await ctx.respond(f"Deleted {count} bot message(s).", ephemeral=True)
    else:
        await ctx.respond("This command can only be used in DMs.", ephemeral=True)


@bot.slash_command(name="user", description="Get member's Information")
async def user(interaction: discord.Interaction, member: discord.Member = None):
    if interaction.guild is None:
        embed = discord.Embed(description=interaction.user.mention, color=discord.Color.blue())
        embed.set_author(name=str(interaction.user), icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(
            name="**Registered**", value=f"{interaction.user.created_at.strftime('%a, %d %b %Y %I:%M %p')}"
        )
        embed.set_footer(text="ID: " + str(interaction.user.id))
        await interaction.response.send_message(embed=embed)
    else:
        if member is None:
            member = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(description=member.mention, color=discord.Color.blue())
        embed.set_author(name=str(member), icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(
            name="**Joined**", value=f"{member.joined_at.strftime(date_format)}"
        )
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="**Join position**", value=f"{str(members.index(member)+1)}")
        embed.add_field(
            name="**Registered**", value=f"{member.created_at.strftime(date_format)}"
        )
        if len(member.roles) > 1:
            role_string = " ".join([r.mention for r in member.roles][1:])
            embed.add_field(
                name=f"**Roles [{len(member.roles) - 1}]**",
                value=f"{role_string}",
                inline=False,
            )
        perm_string = ", ".join(
            [str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]]
        )
        if perm_string:
            embed.add_field(name="**Guild permissions**", value=f"{perm_string}", inline=False)
        embed.set_footer(text="ID: " + str(member.id))
        await interaction.response.send_message(embed=embed)

@bot.slash_command(name="banner", description="Get member's Banner")
async def banner(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    # check if user has a banner and fetch it
    try:
        user = await bot.fetch_user(member.id)
        banner_url = user.banner.url  # The URL of the banner
    except:
        await interaction.response.send_message(
            "> **The user doesn't have a banner.**", ephemeral=True
        )
    # sending the banner
    userAvatar = member.avatar.url
    embed = discord.Embed(
        title="Banner Link", url=banner_url, color=discord.Color.purple()
    )
    embed.set_author(name=member.name, icon_url=userAvatar)
    embed.set_image(url=banner_url)
    embed.set_footer(
        text=f"requested by {interaction.user}", icon_url=interaction.user.avatar.url
    )
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="avatar", description="Get member's Avatar")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if not member:
        member = interaction.user

    user_avatar = member.avatar.url
    embed = discord.Embed(color=discord.Color.dark_gold())
    embed.title = "**Profile Avatar Link**"
    embed.url = user_avatar
    embed.set_author(name=member.name, icon_url=user_avatar)
    embed.set_image(url=user_avatar)
    embed.set_footer(
        text=f"requested by {interaction.user}", icon_url=interaction.user.avatar.url
    )

    display_avatar = member.display_avatar.url

    disavatar_button = discord.ui.Button(
        label="Server's Profile Avatar", style=discord.ButtonStyle.green
    )

    async def show_disavatar(button_interaction: discord.Interaction):
        if button_interaction.user != interaction.user:
            return await button_interaction.response.send_message(
                "This avatar is not for you!", ephemeral=True
            )
        if not display_avatar or display_avatar == user_avatar:
            embed.title = "**Profile Avatar Link**"
            embed.url = display_avatar
            embed.description = "**This user doesn't have a server avatar.**"
            disavatar_button.style = discord.ButtonStyle.gray
            view = discord.ui.View()
        else:
            embed.title = "**Server's Profile Avatar Link**"
            embed.url = display_avatar
            embed.set_image(url=display_avatar)
            disavatar_button.style = discord.ButtonStyle.gray
            view = discord.ui.View()
        await button_interaction.message.edit(embed=embed, view=view)

    disavatar_button.callback = show_disavatar
    view = discord.ui.View(disavatar_button)
    await interaction.response.send_message(embed=embed, view=view)


@bot.slash_command(
    name="private_channel", description="Makes a temporary private channel."
)
async def prvchannel(interaction: discord.Interaction, time: str, channel_name: str):
    # Check if the command was used in a server
    if not interaction.guild:
        return await interaction.response.send_message(
            "> This command can only be used in a server.", ephemeral=True
        )

    guild = interaction.guild
    category = discord.utils.get(interaction.guild.categories)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
    }
    if time:
        get_time = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400,
            "w": 604800,
            "mo": 2592000,
            "y": 31104000,
        }
        timer = time
        a = time[-1]
        b = get_time.get(a)
        c = time[:-1]
        try:
            int(c)
        except:
            return await interaction.response.send_message(
                "> **Type time and time unit s=Seconds,m=Minutes,h=Hours,d=Days,w=Weeks,mo=Month,y=Years correctly**",
                ephemeral=True,
            )
        try:
            sleep = int(b) * int(c)
        except:
            return await interaction.response.send_message(
                "> **Type time and time unit s=Seconds,m=Minutes,h=Hours,d=Days,w=Weeks,mo=Month,y=Years correctly**",
                ephemeral=True,
            )
    channel = await guild.create_text_channel(
        name=channel_name, overwrites=overwrites, category=category
    )
    embed = discord.Embed(
        title="Channel Created! ✅",
        description=f"Private Channel **{channel_name}** has been created for **{timer}**",
        color=discord.Color.nitro_pink(),
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)
    await asyncio.sleep(int(sleep))
    await channel.delete()
    embed = discord.Embed(
        title="Channel Deleted!",
        description=f"Private Channel **{channel_name}** has been deleted after **{timer}**",
        color=discord.Color.nitro_pink(),
    )
    await interaction.followup.send(embed=embed, ephemeral=True)


@bot.slash_command(name="lock", description="Locks a channel.")
async def lock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    channel = channel or interaction.channel
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    if overwrite.send_messages is False:
        return await interaction.response.send_message(
            "> The channel is already locked", ephemeral=True
        )
    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(
        title="🔒 ┃ Channel Locked!",
        description=f"**{channel.mention}** has been locked.",
        color=discord.Color.brand_red(),
    )
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="unlock", description="Unlocks a locked channel.")
async def unlock(interaction: discord.Interaction, channel: discord.TextChannel = None):
    channel = channel or interaction.channel
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    if overwrite.send_messages is True:
        return await interaction.response.send_message(
            "> The channel is already unlocked", ephemeral=True
        )
    overwrite.send_messages = True
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    embed = discord.Embed(
        title="🔓 ┃ Channel Unlocked!",
        description=f"**{channel.mention}** has been unlocked.",
        color=discord.Color.dark_teal(),
    )
    await interaction.response.send_message(embed=embed)


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


@bot.slash_command(name="nya", description="Generate random images of Neko's.")
async def nya(ctx, picture_to_generate: int = 1):
    if isinstance(ctx.channel, discord.DMChannel):
        image_files = [
            f for f in os.listdir("nyan") if f.endswith(".png") or f.endswith(".jpg")
        ]
        chosen_images = random.sample(image_files, picture_to_generate)
        for image in chosen_images:
            await ctx.respond(file=discord.File(f"./nyan/{image}"))
        # image_files = [f for f in os.listdir('nyan') if f.endswith('.png') or f.endswith('.jpg')]
        # chosen_images = random.choice(image_files)
        # await ctx.respond(file=discord.File(f'./nyan/{chosen_images}'))
    else:
        image_files = [
            f for f in os.listdir("nyan") if f.endswith(".png") or f.endswith(".jpg")
        ]
        chosen_images = random.sample(image_files, picture_to_generate)
        for image in chosen_images:
            await ctx.respond(file=discord.File(f"./nyan/{image}"))
        # image_files = [f for f in os.listdir('nyan') if f.endswith('.png') or f.endswith('.jpg')]
        # chosen_images = random.choice(image_files)
        # await ctx.respond(file=discord.File(f'./nyan/{chosen_images}'))


# Testing



# DeepL Translation

try:
    with open(JSON_PATH, "r") as f:
        selected_lang = json.load(f)
except FileNotFoundError:
    selected_lang = {"default": {"language": "JA", "translator": "DeepL"}}
    with open(JSON_PATH, "w") as f:
        json.dump(selected_lang, f)


class LanguageDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        lang = selected_lang.get(user_id, {}).get(
            "language"
        )  # get user's selected language
        options = [
            discord.SelectOption(
                label="Japanese",
                description="Japanese Language",
                emoji="🇯🇵",
                value="JA",
                default=lang == "JA",
            ),
            discord.SelectOption(
                label="Korean",
                description="Korean Language",
                emoji="🇰🇷",
                value="KO",
                default=lang == "KO",
            ),
            discord.SelectOption(
                label="English",
                description="English Language",
                emoji="🇺🇸",
                value="EN",
                default=lang == "EN",
            ),
            discord.SelectOption(
                label="Chinese (Simplified)",
                description="Chinese Language",
                emoji="🇨🇳",
                value="zh-CN",
                default=lang == "zh-CN",
            ),
            discord.SelectOption(
                label="Chinese (Traditional)",
                description="Chinese(Traditional) Language",
                emoji="🇨🇳",
                value="zh-TW",
                default=lang == "zh-TW",
            ),
        ]
        super().__init__(placeholder="Select language to translate...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_lang:
            selected_lang[user_id] = {"language": "JA", "translator": "DeepL"}
        if isinstance(selected_lang[user_id], dict):
            selected_lang[user_id]["language"] = self.values[0]
            with open(JSON_PATH, "w") as f:
                json.dump(selected_lang, f)
            selected_option = next(
                option for option in self.options if option.value == self.values[0]
            )
            await interaction.response.send_message(
                f"Selected language: {selected_option.label} {selected_option.emoji}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your selected language and translator.",
                ephemeral=True,
            )


class TranslatorDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(JSON_PATH, "r") as f:
            selected_trans = json.load(f)
        trans = selected_trans.get(user_id, {}).get("translator")
        options = [
            discord.SelectOption(
                label="DeepL",
                description="Translate using DeepL",
                emoji="<:DeepL:1092335121081839647> ",
                value="DeepL",
                default=trans == "DeepL",
            ),
            discord.SelectOption(
                label="Google Translate",
                description="Translate using Google Translate",
                emoji="<:Google_Translate:1092335419636584480> ",
                value="Google Translate",
                default=trans == "Google Translate",
            ),
        ]
        super().__init__(placeholder="Select translator...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(JSON_PATH, "r") as f:
            selected_lang = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_lang:
            selected_lang[user_id] = {"language": "JA", "translator": "DeepL"}
        if isinstance(selected_lang[user_id], dict):
            selected_lang[user_id]["translator"] = self.values[0]
            with open(JSON_PATH, "w") as f:
                json.dump(selected_lang, f)
            selected_options = [
                option for option in self.options if option.value in self.values
            ]
            selected_labels = [option.label for option in selected_options]
            selected_emojis = [str(option.emoji) for option in selected_options]
            await interaction.response.send_message(
                f"Selected translator: {', '.join(selected_labels)} {' '.join(selected_emojis)}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your selected language and translator.",
                ephemeral=True,
            )


class DropdownView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__()
        self.add_item(TranslatorDropdown(user_id=user_id))
        self.add_item(LanguageDropdown(user_id=user_id))


@bot.slash_command(name="tlsettings", description="Translator Settings")
async def tlsettings(ctx: discord.ApplicationContext):
    """Sends a message with our dropdowns that contain language and translator options."""
    view = DropdownView(str(ctx.author.id))
    embed = discord.Embed(
        title="Translation Options",
        description="Select a language and translator to use for translation:",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Translator:", value="DeepL", inline=False)
    embed.add_field(
        name="Languages:",
        value="Japanese,English,Chinese(Simplified),Chinese(Traditional)",
        inline=False,
    )
    await ctx.respond(embed=embed, view=view, ephemeral=True)


async def translate_text(text: str, target_lang: str, translator: str) -> str:
    if translator == "DeepL":
        auth_key = os.environ.get("DeepL_API")
        if target_lang in ("zh-TW", "zh-CN"):
            target_lang = "ZH"
            result = deepl.Translator(auth_key).translate_text(
                text, target_lang=target_lang
            )
        elif target_lang == "EN":
            target_lang = "EN-US"
            result = deepl.Translator(auth_key).translate_text(
                text, target_lang=target_lang
            )
        else:
            result = deepl.Translator(auth_key).translate_text(
                text, target_lang=target_lang
            )
        return result.text
    if translator == "Google Translate":
        if target_lang == "zh-TW":
            target_lang = "zh-TW"
            result = GoogleTranslator(source="auto", target=target_lang).translate(
                text=text
            )
        elif target_lang == "zh-CN":
            target_lang = "zh-CN"
            result = GoogleTranslator(source="auto", target=target_lang).translate(
                text=text
            )
        else:
            result = GoogleTranslator(
                source="auto", target=target_lang.lower()
            ).translate(text=text)
        return result
    return f"Invalid translator selected: {translator}"


@bot.slash_command(
    name="translate", description="Gura helps you to translate messages"
)
async def translate(ctx: discord.ApplicationContext, message: str):
    """Translates a message to the selected language using the selected translator."""
    # Retrieve the user's selected language and translator from the JSON file using their user id as the key
    with open(JSON_PATH, "r") as f:
        selected_lang = json.load(f)
    user_language = selected_lang.get(str(ctx.author.id), selected_lang["default"])[
        "language"
    ]
    user_translator = selected_lang.get(str(ctx.author.id), selected_lang["default"])[
        "translator"
    ]
    # Translate the message to the user's selected language using the selected translator
    translated_text = await translate_text(message, user_language, user_translator)

    # Create an embed with the input text and the translated text
    embed = discord.Embed(title="**Translation**", color=discord.Color.nitro_pink())
    embed.add_field(name="**Input Text**", value=f"`{message}\n`", inline=False)
    embed.add_field(
        name="**Translated Text**", value=f"`{translated_text}\n`", inline=False
    )
    embed.set_footer(
        text=f"Requested by {ctx.interaction.user.name}",
        icon_url=ctx.interaction.user.display_avatar.url,
    )
    # Send the embed as a response to the slash command
    await ctx.respond(embed=embed)


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


# Waifu Generation
try:
    with open(WAIFU_PATH, "r") as f:
        waifu = json.load(f)
except FileNotFoundError:
    waifu = {
        "default": {
            "engine": "waifupics",
            "category": "waifu",
            "type": "sfw",
            "gif": "false",
        }
    }
    with open(WAIFU_PATH, "w") as f:
        json.dump(waifu, f)


class WaifuEngineDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(WAIFU_PATH, "r") as f:
            selected_engine = json.load(f)
        engine = selected_engine.get(user_id, {}).get("engine")
        options = [
            discord.SelectOption(
                label="Waifu Pics",
                description="Use waifu.pics to generate waifus",
                emoji="🎏",
                value="waifupics",
                default=engine == "waifupics",
            ),
            discord.SelectOption(
                label="Waifu Im",
                description="Use waifu.im to generate waifus",
                emoji="🌸",
                value="waifuim",
                default=engine == "waifuim",
            ),
        ]
        super().__init__(placeholder="Select Engine...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(WAIFU_PATH, "r") as f:
            selected_engine = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_engine:
            selected_engine[user_id] = {
                "engine": "waifupics",
                "category": "waifu",
                "type": "sfw",
                "gif": "false",
            }
        if isinstance(selected_engine[user_id], dict):
            selected_engine[user_id]["engine"] = self.values[0]
            with open(WAIFU_PATH, "w") as f:
                json.dump(selected_engine, f)
            selected_options = [
                option for option in self.options if option.value in self.values
            ]
            selected_labels = [option.label for option in selected_options]
            selected_emojis = [str(option.emoji) for option in selected_options]
            await interaction.response.send_message(
                f"Selected Engine: {', '.join(selected_labels)} {' '.join(selected_emojis)}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your settings.", ephemeral=True
            )


class CategoryDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(WAIFU_PATH, "r") as f:
            try:
                waifu_data = json.load(f).get(user_id, {})
            except json.decoder.JSONDecodeError:
                print("Error: Could not decode JSON file.")
                waifu_data = {}
            selected_engine = waifu_data.get("engine")
            category = waifu_data.get("category")
            type = waifu_data.get("type")
        if selected_engine == "waifupics" and type == "sfw":
            options = [
                discord.SelectOption(
                    label="Hug",
                    description="Hug",
                    value="hug",
                    default=category == "hug",
                ),
                discord.SelectOption(
                    label="Blush",
                    description="Blush",
                    value="blush",
                    default=category == "blush",
                ),
                discord.SelectOption(
                    label="Kiss",
                    description="Kiss",
                    value="kiss",
                    default=category == "kiss",
                ),
                discord.SelectOption(
                    label="Lick",
                    description="Lick",
                    value="lick",
                    default=category == "lick",
                ),
                discord.SelectOption(
                    label="Pat",
                    description="Pat",
                    value="pat",
                    default=category == "pat",
                ),
                discord.SelectOption(
                    label="Smug",
                    description="Smug",
                    value="smug",
                    default=category == "smug",
                ),
                discord.SelectOption(
                    label="Bonk",
                    description="Bonk",
                    value="bonk",
                    default=category == "bonk",
                ),
                discord.SelectOption(
                    label="Waifu",
                    description="Waifu",
                    value="waifu",
                    default=category == "waifu",
                ),
                discord.SelectOption(
                    label="Neko",
                    description="Neko",
                    value="neko",
                    default=category == "neko",
                ),
                discord.SelectOption(
                    label="Megumin",
                    description="Megumin",
                    value="megumin",
                    default=category == "megumin",
                ),
                discord.SelectOption(
                    label="Cuddle",
                    description="Cuddle",
                    value="cuddle",
                    default=category == "cuddle",
                ),
                discord.SelectOption(
                    label="Cry",
                    description="Cry",
                    value="cry",
                    default=category == "cry",
                ),
                discord.SelectOption(
                    label="Awoo",
                    description="Awoo",
                    value="awoo",
                    default=category == "awoo",
                ),
                discord.SelectOption(
                    label="Yeet",
                    description="Yeet",
                    value="yeet",
                    default=category == "yeet",
                ),
                discord.SelectOption(
                    label="Smile",
                    description="Smile",
                    value="smile",
                    default=category == "smile",
                ),
                discord.SelectOption(
                    label="Wave",
                    description="Wave",
                    value="wave",
                    default=category == "wave",
                ),
                discord.SelectOption(
                    label="Highfive",
                    description="Highfive",
                    value="highfive",
                    default=category == "highfive",
                ),
                discord.SelectOption(
                    label="Handhold",
                    description="Handhold",
                    value="handhold",
                    default=category == "handhold",
                ),
                discord.SelectOption(
                    label="Bite",
                    description="Bite",
                    value="bite",
                    default=category == "bite",
                ),
                discord.SelectOption(
                    label="Slap",
                    description="Slap",
                    value="slap",
                    default=category == "slap",
                ),
                discord.SelectOption(
                    label="Kill",
                    description="Kill",
                    value="kill",
                    default=category == "kill",
                ),
                discord.SelectOption(
                    label="Happy",
                    description="Happy",
                    value="happy",
                    default=category == "happy",
                ),
                discord.SelectOption(
                    label="Wink",
                    description="Wink",
                    value="wink",
                    default=category == "wink",
                ),
                discord.SelectOption(
                    label="Poke",
                    description="Poke",
                    value="poke",
                    default=category == "poke",
                ),
                discord.SelectOption(
                    label="Dance",
                    description="Dance",
                    value="dance",
                    default=category == "dance",
                ),
            ]
        elif selected_engine == "waifupics" and type == "nsfw":
            options = [
                discord.SelectOption(
                    label="Trap",
                    description="Trap",
                    value="trap",
                    default=category == "trap",
                ),
                discord.SelectOption(
                    label="Blowjob",
                    description="Blowjob",
                    value="blowjob",
                    default=category == "blowjob",
                ),
                discord.SelectOption(
                    label="Waifu",
                    description="Waifu",
                    value="waifu",
                    default=category == "waifu",
                ),
                discord.SelectOption(
                    label="Neko",
                    description="Neko",
                    value="neko",
                    default=category == "neko",
                ),
            ]
        elif selected_engine == "waifuim" and type == "sfw":
            options = [
                discord.SelectOption(
                    label="Maid",
                    description="Maid",
                    value="maid",
                    default=category == "maid",
                ),
                discord.SelectOption(
                    label="Waifu",
                    description="Waifu",
                    value="waifu",
                    default=category == "waifu",
                ),
                discord.SelectOption(
                    label="Marin Kitagawa",
                    description="Marin Kitagawa",
                    value="marin-kitagawa",
                    default=category == "marin-kitagawa",
                ),
                discord.SelectOption(
                    label="Mori Calliope",
                    description="Mori Calliope",
                    value="mori-calliope",
                    default=category == "mori-calliope",
                ),
                discord.SelectOption(
                    label="Raiden Shogun",
                    description="Raiden Shogun",
                    value="raiden-shogun",
                    default=category == "raiden-shogun",
                ),
                discord.SelectOption(
                    label="Oppai",
                    description="Oppai",
                    value="opai",
                    default=category == "Oppai",
                ),
                discord.SelectOption(
                    label="Selfies",
                    description="Selfies",
                    value="selfies",
                    default=category == "selfies",
                ),
                discord.SelectOption(
                    label="Uniform",
                    description="Uniform",
                    value="uniform",
                    default=category == "uniform",
                ),
            ]
        elif selected_engine == "waifuim" and type == "nsfw":
            options = [
                discord.SelectOption(
                    label="Ass",
                    description="Ass",
                    value="ass",
                    default=category == "ass",
                ),
                discord.SelectOption(
                    label="Hentai",
                    description="Hentai",
                    value="hentai",
                    default=category == "hentai",
                ),
                discord.SelectOption(
                    label="Mlif",
                    description="Mlif",
                    value="mlif",
                    default=category == "mlif",
                ),
                discord.SelectOption(
                    label="Oral",
                    description="oral",
                    value="oral",
                    default=category == "oral",
                ),
                discord.SelectOption(
                    label="Paizuri",
                    description="paizuri",
                    value="paizuri",
                    default=category == "paizuri",
                ),
                discord.SelectOption(
                    label="Ecchi",
                    description="Ecchi",
                    value="ecchi",
                    default=category == "ecchi",
                ),
                discord.SelectOption(
                    label="Ero",
                    description="Ero",
                    value="ero",
                    default=category == "ero",
                ),
            ]
        else:
            options = [
                discord.SelectOption(
                    label="Select an Engine First...",
                    value="disabled",
                    description="This option is disabled",
                    emoji="❌",
                )
            ]

        super().__init__(placeholder="Select Waifu category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(WAIFU_PATH, "r") as f:
            selected_cat = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_cat:
            selected_cat[user_id] = {
                "engine": "waifupics",
                "category": "waifu",
                "type": "sfw",
                "gif": "false",
            }
        if isinstance(selected_cat[user_id], dict):
            selected_cat[user_id]["category"] = self.values[0]
            with open(WAIFU_PATH, "w") as f:
                json.dump(selected_cat, f)
            selected_option = next(
                option for option in self.options if option.value == self.values[0]
            )
            await interaction.response.send_message(
                f"Selected Category: {selected_option.label}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your selected settings",
                ephemeral=True,
            )


class TypeDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(WAIFU_PATH, "r") as f:
            selected_type = json.load(f)
        type = selected_type.get(user_id, {}).get("type")
        options = [
            discord.SelectOption(
                label="Safe For Work",
                description="Safe For Work Pictures",
                value="sfw",
                default=type == "sfw",
            ),
            discord.SelectOption(
                label="Not Safe For Work",
                description="Not Safe For Work Pictures",
                value="nsfw",
                default=type == "nsfw",
            ),
        ]
        super().__init__(placeholder="Select Type of Image...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(WAIFU_PATH, "r") as f:
            selected_type = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_type:
            selected_type[user_id] = {
                "engine": "waifupics",
                "category": "waifu",
                "type": "sfw",
                "gif": "false",
            }
        if isinstance(selected_type[user_id], dict):
            selected_type[user_id]["type"] = self.values[0]
            with open(WAIFU_PATH, "w") as f:
                json.dump(selected_type, f)
            selected_options = [
                option for option in self.options if option.value in self.values
            ]
            selected_labels = [option.label for option in selected_options]
            selected_emojis = [str(option.emoji) for option in selected_options]
            await interaction.response.send_message(
                f"Selected Type: {', '.join(selected_labels)}", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your settings.", ephemeral=True
            )


class GifDropdown(discord.ui.Select):
    def __init__(self, user_id: str):
        with open(WAIFU_PATH, "r") as f:
            selected_gif = json.load(f)
        gif = selected_gif.get(user_id, {}).get("gif")
        options = [
            discord.SelectOption(
                label="Enable Gif",
                description="Enable Gif for Waifu.im",
                emoji="✅",
                value="true",
                default=gif == "true",
            ),
            discord.SelectOption(
                label="Disable Gif",
                description="Disable Gif for Waifu.im",
                emoji="❌",
                value="false",
                default=gif == "false",
            ),
        ]
        super().__init__(placeholder="Select Gif Status...", options=options)

    async def callback(self, interaction: discord.Interaction):
        with open(WAIFU_PATH, "r") as f:
            selected_gif = json.load(f)
        user_id = str(interaction.user.id)
        if user_id not in selected_gif:
            selected_gif[user_id] = {
                "engine": "waifupics",
                "category": "waifu",
                "type": "sfw",
                "gif": "false",
            }
        if isinstance(selected_gif[user_id], dict):
            selected_gif[user_id]["gif"] = self.values[0]
            with open(WAIFU_PATH, "w") as f:
                json.dump(selected_gif, f)
            selected_options = [
                option for option in self.options if option.value in self.values
            ]
            selected_labels = [option.label for option in selected_options]
            selected_emojis = [str(option.emoji) for option in selected_options]
            await interaction.response.send_message(
                f"Selected Gif: {' '.join(selected_emojis)}{', '.join(selected_labels)}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "An error occurred while retrieving your settings.", ephemeral=True
            )


class WaifuView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__()
        self.add_item(WaifuEngineDropdown(user_id=user_id))
        self.add_item(CategoryDropdown(user_id=user_id))
        self.add_item(TypeDropdown(user_id=user_id))
        self.add_item(GifDropdown(user_id=user_id))


@bot.slash_command(name="waifusettings", description="Waifu Settings")
async def tlsettings(ctx: discord.ApplicationContext):
    """Sends a message with our dropdowns that contain language and translator options."""
    view = WaifuView(str(ctx.author.id))
    embed = discord.Embed(
        title="Waifu Options",
        description="Select an Engine, Category and Type:",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Engine:", value="Waifu.pics,Waifu.im", inline=False)
    embed.add_field(
        name="Categories(Waifu.pics):",
        value=", ".join(waifupic_categories),
        inline=False,
    )
    embed.add_field(
        name="Type(Waifu.pics):", value=", ".join(waifupic_types), inline=False
    )
    embed.add_field(
        name="Categories(Waifu.im):", value=", ".join(waifuim_categories), inline=False
    )
    embed.add_field(
        name="Type(Waifu.im):", value=", ".join(waifuim_types), inline=False
    )
    embed.add_field(name="Gif(Waifu.im):", value="Enable,Disable", inline=False)
    await ctx.respond(embed=embed, view=view, ephemeral=True)


@bot.slash_command(name="waifu", description="Generate Images of Waifu's")
async def waifu(ctx, context=None, type=None, amount: int = 1):
    user_id = str(ctx.author.id)
    # Load the user settings from the JSON file
    with open("Waifu.json", "r") as f:
        user_settings = json.load(f).get(user_id, {})
    # Get the engine, category and type from the user settings or the default settings
    engine = user_settings.get("engine", "waifupic")
    category = user_settings.get("category", "waifu")
    gif = user_settings.get("gif", "false")
    if context:
        category = context.lower()
    if not type:
        type = user_settings.get("type", "sfw")
    # Check if the engine, category and type are valid, otherwise show an embed with the valid options
    if engine == "waifupics":
        if category not in waifupic_categories or type not in waifupic_types:
            embed = discord.Embed(
                title="Invalid category or type",
                description=f"Valid categories: {', '.join(waifupic_categories)}\nValid types: {', '.join(waifupic_types)}",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        # Generate the specified amount of images and send them as an embed
        for i in range(amount):
            response = requests.get(f"https://api.waifu.pics/{type}/{category}")
            image_url = response.json()["url"]
            embed = discord.Embed(
                title=f"{category.capitalize()} image ({type})",
                color=discord.Color.blurple(),
            )
            embed.add_field(name="**Category**", value=f"**{category.capitalize()}**")
            embed.set_image(url=image_url)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.send(embed=embed)
    elif engine == "waifuim":
        if category not in waifuim_categories or type not in waifuim_types:
            embed = discord.Embed(
                title="Invalid category or type",
                description=f"Valid categories: {', '.join(waifuim_categories)}\nValid types: {', '.join(waifuim_types)}",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
        # Generate the specified amount of images (up to 1 if gif is enabled) and send them as an embed
        if gif == "true":
            amount = 1
        else:
            pass
        async with aiohttp.ClientSession() as session:
            params = {
                "included_tags": category,
                "is_nsfw": "true" if type == "nsfw" else "false",
                "gif": "true" if gif else "false",
            }
            async with session.get("https://api.waifu.im/search/", params=params) as r:
                data = await r.json(loads=orjson.loads)
        for i in range(amount):
            image_url = data.get("images", [])[i].get("url")
            if image_url is not None:
                embed = discord.Embed(
                    title=f"{category.capitalize()} image ({type})",
                    color=discord.Color.og_blurple(),
                )
                embed.add_field(
                    name="**Category**", value=f"**{category.capitalize()}**"
                )
                embed.set_image(url=image_url)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Invalid engine",
            description="Valid engines: waifupic, waifuim",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


# Search Anime and Manga
@bot.slash_command(
    name="anime", description="Gura helps you to search anime using AniList"
)
async def al_anime(interaction, *, name):
    """Searches Anilist for an Anime."""
    try:
        result = await klient.search_anime(name, popularity=True, allow_adult=True)
    except MediaNotFound:
        return await interaction.response.send_message(
            ":exclamation: Anime was not found!"
        )
    except Exception as e:
        return await interaction.response.send_message(
            f":exclamation: An unknown error occurred:\n{e}"
        )

    if interaction.response.is_done():
        return  # Interaction is no longer available, so stop processing

    # if len(result.description) > 1024:
    #     result.description = result.description[:1024 - (len(result.site_url) + 7)] + f"[...]({result.site_url})"
    if result.genres:
        genere = f"***{', '.join(result.genres)}***\n"
    if result.description:
        synopsis = f"{result.description[:250]}... [(full)]({result.site_url})"
    if result.cover_color:
        color = int(result.cover_color.replace("#", ""), 16)
    else:
        color = discord.Color.nitro_pink()  # "0x02a9ff"
    embed = discord.Embed(
        title=result.title["english"] or result.title["romaji"], colour=color
    )
    embed.description = genere
    embed.url = result.site_url
    embed.add_field(name="Japanese Title", value=result.title["native"], inline=True)
    embed.add_field(
        name="Type",
        value=str(result.format.name).replace("_", " ").capitalize(),
        inline=True,
    )
    embed.add_field(name="Episodes", value=result.episodes or "?", inline=True)
    embed.add_field(
        name="Score",
        value=str(result.average_score / 10) + " / 10" if result.average_score else "?",
        inline=False,
    )
    embed.add_field(
        name="Status",
        value=str(result.status.name).replace("_", " ").capitalize(),
        inline=True,
    )
    (year, month, day) = result.start_date.values()
    aired = f"{day}/{month}/{year}"
    (year, month, day) = (
        result.end_date.values() if result.end_date["day"] else ("?", "?", "?")
    )
    aired += f" - {day}/{month}/{year}"
    embed.add_field(name="Aired", value=aired, inline=True)
    embed.add_field(name="Synopsis", value=synopsis, inline=False)
    embed.add_field(name="Link", value=result.site_url, inline=False)
    embed.set_author(name="Anilist", icon_url=AL_ICON)
    embed.set_thumbnail(url=result.cover_image)
    embed.set_image(url=f"https://img.anili.st/media/{result.id}")
    embed.set_footer(
        text=f"Requested by {interaction.user.name}",
        icon_url=interaction.user.display_avatar.url,
    )
    if interaction.response.is_done():
        return  # Interaction is no longer available, so stop processing
    await interaction.response.defer()
    await interaction.followup.send(embed=embed)


@bot.slash_command(
    name="manga", description="Gura helps you to search manga using AniList"
)
async def al_anime(interaction, *, name):
    """Searches Anilist for an Anime."""
    try:
        result = await klient.search_manga(name, popularity=True, allow_adult=True)
    except MediaNotFound:
        return await interaction.response.send_message(
            ":exclamation: Anime was not found!"
        )
    except Exception as e:
        return await interaction.response.send_message(
            f":exclamation: An unknown error occurred:\n{e}"
        )

    if interaction.response.is_done():
        return  # Interaction is no longer available, so stop processing

    # if len(result.description) > 1024:
    #     result.description = result.description[:1024 - (len(result.site_url) + 7)] + f"[...]({result.site_url})"
    if result.genres:
        genere = f"***{', '.join(result.genres)}***\n"
    if result.description:
        synopsis = f"{result.description[:250]}... [(full)]({result.site_url})"
    if result.cover_color:
        color = int(result.cover_color.replace("#", ""), 16)
    else:
        color = discord.Color.nitro_pink()  # "0x02a9ff"
    embed = discord.Embed(
        title=result.title["english"] or result.title["romaji"], colour=color
    )
    embed.description = genere
    embed.url = result.site_url
    embed.add_field(name="Japanese Title", value=result.title["native"], inline=True)
    embed.add_field(
        name="Type",
        value=str(result.format.name).replace("_", " ").capitalize(),
        inline=True,
    )
    embed.add_field(name="Chapters", value=result.chapters or "?", inline=True)
    embed.add_field(name="Volumes", value=result.volumes or "?", inline=True)
    embed.add_field(
        name="Score",
        value=str(result.average_score / 10) + " / 10" if result.average_score else "?",
        inline=False,
    )
    embed.add_field(
        name="Status",
        value=str(result.status.name).replace("_", " ").capitalize(),
        inline=True,
    )
    (year, month, day) = result.start_date.values()
    published = f"{day}/{month}/{year}"
    (year, month, day) = (
        result.end_date.values() if result.end_date["day"] else ("?", "?", "?")
    )
    published += f" - {day}/{month}/{year}"
    embed.add_field(name="Published", value=published, inline=True)
    embed.add_field(name="Synopsis", value=synopsis, inline=False)
    embed.add_field(name="Link", value=result.site_url, inline=False)
    embed.set_author(name="Anilist", icon_url=AL_ICON)
    embed.set_thumbnail(url=result.cover_image)
    embed.set_image(url=f"https://img.anili.st/media/{result.id}")
    embed.set_footer(
        text=f"Requested by {interaction.user.name}",
        icon_url=interaction.user.display_avatar.url,
    )
    if interaction.response.is_done():
        return  # Interaction is no longer available, so stop processing
    await interaction.response.defer()
    await interaction.followup.send(embed=embed)

## Genshin
@bot.slash_command(name="genshin_daily", description="Receive Hoyolab daily check-in reward")
async def genshin_daily_slash(ctx):
    cookies = Hoyolab_Cookies.get(ctx.author.id)
    hashed_ltuid = cookies.get('ltuid')
    hashed_ltoken = cookies.get('ltoken')
    ltuid = decrypt(hashed_ltuid, ctx.author.id)
    ltoken = decrypt(hashed_ltoken, ctx.author.id)
    if cookies is None:
        await ctx.respond(f"Cookies are not set for {ctx.author}.Please set cookies with '/set_cookies'",empheral=True)
        return
    client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},game=genshin.Game.GENSHIN)
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
            text=f"Requested by {ctx.interaction.user.name}",
            icon_url=ctx.interaction.user.display_avatar.url,
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)
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
                text=f"Requested by {ctx.interaction.user.name}",
            icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Genshin Hoyolab Daily Check-In",
                color=0xFFB6C1,
            )
            embed.add_field(name="An error has occured:", value=f"{e}",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
            icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
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
            text=f"Requested by {ctx.interaction.user.name}",
            icon_url=ctx.interaction.user.display_avatar.url,
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)
        
@bot.slash_command(name="set_cookies", description="Set cookies for Genshin Impact API requests")
async def set_cookies(ctx, ltuid: int, ltoken: str):
    hashed_ltuid = encrypt(str(ltuid), ctx.author.id)
    hashed_ltoken = encrypt(ltoken, ctx.author.id)
    Hoyolab_Cookies[ctx.author.id] = {"ltuid": hashed_ltuid, "ltoken": hashed_ltoken}
    embed = discord.Embed(
            title="Hoyolab Cookies",
            description="Cookies set successfully!",
            color=0xFFB6C1,
        )
    embed.set_footer(
        text=f"Requested by {ctx.interaction.user.name}",
        icon_url=ctx.interaction.user.display_avatar.url,
    )
    await ctx.response.send_message(embed=embed, ephemeral=True)
    
bot.run(os.environ.get("Discord_Token"))
