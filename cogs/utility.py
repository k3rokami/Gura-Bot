import discord
import datetime
import pytz
import logging
import deepl
import pysaucenao
import deep_translator
import requests
import aiohttp
import genshin
import orjson
import asyncio
import platform
from discord.commands import SlashCommandGroup
from discord.ext import commands

singapore_tz = pytz.timezone("Asia/Singapore")
start_time = datetime.datetime.now(singapore_tz)

class UtilityMenu(commands.Cog):
    def __init__(self, bot, version):
        self.bot = bot
        self.version = version
        
    utility = SlashCommandGroup("utility", "Various commands to get more information on Gura!")
    
    @utility.command(name="ping", description="Gura's Latency")
    async def ping(self, ctx):
        await ctx.respond(
            embed=discord.Embed(
                description=f"Ping: {self.bot.latency*1000:.2f}ms", color=discord.Color.purple()
            ),
            ephemeral=True,
        )
        
    @utility.command(name="about", description="Returns information about Gura🦈")
    async def about(self, ctx):
        text_channel = 0
        # voice_channel = 0
        # stage_channel = 0

        for channel in self.bot.get_all_channels():
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
            value=f"\n<:Servers:1091947846078566563> Servers : `{len(self.bot.guilds)}`"
            f"\n<:Users:1091947828462506044> Users : `{len(self.bot.users)}`"
            f"\n<:Text_Channel:1091947813249765416> Text channels : `{text_channel}`"
            #   f"\n<:Voice_Channel:1091947799710543884> Voice channels : `{voice_channel}`"
            #   f"\n<:Stage_Channel:1091947859156422816> Stage channels : `{stage_channel}`"
            f"\n<:Commands:1091947872670470216> Commands : `{len(self.bot.commands)+len(self.bot.application_commands)}`"
            f"\n<:GawrGuraHeart:1092448958816722995>  Gawr Gura's Version : `{self.version.capitalize()}`"
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
            value=f"`Py-Cord {'.'.join(discord.__version__.split('.')[0:3])}`\n`PySauceNao {pysaucenao.__version__}`\n`DeepL {deepl.__version__}`\n`Deep Translator {deep_translator.__version__}`\n`Genshin {genshin.__version__}`",
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


    @utility.command(name="delete-messages", description="Delete messages sent by the bot in DM channel.")
    async def delete_messages(self, ctx, count: int = 1):
        # Check if the command was executed in a DM channel
        if ctx.channel.type in (discord.ChannelType.private, discord.ChannelType.group):
            # Get the bot's messages in the DM channel
            bot_messages = [
                msg
                for msg in await ctx.channel.history(limit=None).flatten()
                if msg.author == self.bot.user
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


    @utility.command(name="user", description="Get member's Information")
    async def user(self, interaction: discord.Interaction, member: discord.Member = None):
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

    @utility.command(name="banner", description="Get member's Banner")
    async def banner(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        # check if user has a banner and fetch it
        try:
            user = await self.bot.fetch_user(member.id)
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


    @utility.command(name="avatar", description="Get member's Avatar")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
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


    @utility.command(name="private_channel", description="Makes a temporary private channel.")
    async def prvchannel(self, interaction: discord.Interaction, time: str, channel_name: str):
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


    @utility.command(name="lock", description="Locks a channel.")
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
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


    @utility.command(name="unlock", description="Unlocks a locked channel.")
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
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
        
def setup(bot):
    bot.add_cog(UtilityMenu(bot))