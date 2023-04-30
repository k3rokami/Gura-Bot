from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import option
import discord

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
            
class HelpMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    help = SlashCommandGroup("help", "Various help commands for Gura!")
        
    @help.command(name="start", description="Gura's help command.")
    async def start(self, interaction: discord.Interaction):
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
        
    @help.command(name="help_moderation", description="Gura's moderation category help.")
    @option("command",
        description="Choose a command to get info about it.",
        choices=["Lock", "Unlock"],
    )
    async def moderation(self, interaction: discord.Interaction, command: str):
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


    @help.command(name="waifu", description="Gura's waifu image category help.")
    @option(
        "command",
        description="Choose a command to get info about it.",
        choices=["waifu", "waifusettings"],
    )
    async def waifu(self, interaction: discord.Interaction, command: str):
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



    @help.command(name="search", description="Gura's image generation category help.")
    @option(
        "command",
        description="Choose a command to get info about it.",
        choices=["anime", "manga"],
    )
    async def search(self, interaction: discord.Interaction, command: str):
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


    @help.command(name="translate", description="Gura's translation category help.")
    @option("command",
        description="Choose a command to get info about it.",
        choices=["translate", "tlsettings"],
    )
    async def translate(self, interaction: discord.Interaction, command: str):
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

    @help.command(name="help_utility", description="Gura's image generation category help.")
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
    async def utility(self, interaction: discord.Interaction, command: str):
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


    @help.command(name="serverinformation", description="Gura's image generation category help.")
    @option(
        "command",
        description="Choose a command to get info about it.",
        choices=["about", "ping"],
    )
    async def serverinformation(self, interaction: discord.Interaction, command: str):
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

def setup(bot):
    bot.add_cog(HelpMenu(bot))