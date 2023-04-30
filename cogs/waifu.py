import discord
import json
import aiohttp
import orjson
import requests

from discord.commands import SlashCommandGroup
from discord.ext import commands

WAIFU_PATH = "./Waifu.json"
waifupic_categories = ["waifu","neko","shinobu","megumin","bully","cuddle","cry","hug","awoo","kiss","lick","pat","smug","bonk","yeet","blush","smile","wave","highfive","handhold","nom","bite","glomp","slap","kill","kick","happy","wink","poke","dance","cringe","trap","blowjob"]
waifupic_types = ["sfw", "nsfw"]
waifuim_categories = ["maid","waifu","marin-kitagawa","mori-calliope","raiden-shogun","selfies","uniform","ass","hentai","mlif","oral","paizuri","ecchi","ero"]
waifuim_types = ["sfw", "nsfw"]

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

class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    waifu = SlashCommandGroup("waifu", "Generate waifu images!")
    
    @waifu.command(name="settings", description="Waifu Image Generator Settings")
    async def waifusettings(self, ctx: discord.ApplicationContext):
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


    @waifu.command(name="generate", description="Generate Images of Waifu's")
    async def generate(self, ctx, context=None, type=None, amount: int = 1):
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
    
def setup(bot):
    bot.add_cog(Waifu(bot))