import requests
import hashlib
import base64
import genshin
import discord

from cogs.genshin import Hoyolab_Cookies,encrypt,decrypt
from cryptography.fernet import Fernet
from discord.commands import SlashCommandGroup
from discord.ext import commands

class HonkaiImpact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    honkai = SlashCommandGroup("honkai", "Various Hoyolab Honkai Impact Commands")
    @honkai.command(name="daily", description="Receive Hoyolab daily check-in reward")
    async def daily(self, ctx):
        cookies = Hoyolab_Cookies.get(ctx.author.id)
        hashed_ltuid = cookies.get('ltuid')
        hashed_ltoken = cookies.get('ltoken')
        ltuid = decrypt(hashed_ltuid, ctx.author.id)
        ltoken = decrypt(hashed_ltoken, ctx.author.id)
        if cookies is None:
            await ctx.respond(f"Cookies are not set for {ctx.author}.Please set cookies with '/honkai cookies'",empheral=True)
            return
        client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},game=genshin.Game.HONKAI)
        try:
            reward = await client.claim_daily_reward()
        except genshin.AlreadyClaimed:
            # print("Daily reward already claimed")
            signed_in, claimed_rewards = await client.get_reward_info()
            embed = discord.Embed(
                title="Honkai Hoyolab Daily Check-In",
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
                    title="Honkai Hoyolab Daily Check-In",
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
                    title="Honkai Hoyolab Daily Check-In",
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
            claimed_rewards = await client.get_reward_info()
            embed = discord.Embed(
                title="Honkai Hoyolab Daily Check-In",
                color=0xFFB6C1,
            )
            embed.add_field(name="Reward:", value=f"{reward.amount}x {reward.name}",inline=False)
            embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            await ctx.response.send_message(embed=embed, ephemeral=True)
            
    @honkai.command(name="cookies", description="Set cookies for Honkai Impact API requests")
    async def cookies(self, ctx, ltuid: int, ltoken: str):
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
            
def setup(bot):
    bot.add_cog(HonkaiImpact(bot))