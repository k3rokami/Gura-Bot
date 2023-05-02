import genshin
import discord
import datetime

from cogs.genshin import encrypt,decrypt
from cogs.hoyolab import Hoyolab_Cookies
from discord.commands import SlashCommandGroup
from discord.ext import commands

class HonkaiImpact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    honkai = SlashCommandGroup("honkai", "Various Hoyolab Honkai Impact Commands")
    
    @honkai.command(name="daily", description="Receive Hoyolab daily check-in reward")
    async def daily(self, ctx):
        cookies = Hoyolab_Cookies.get(ctx.author.id)
        if cookies == None:
            embed = discord.Embed(
                title="Genshin Hoyolab Daily Check-In",
                color=0xFFB6C1,
            )
            embed.add_field(name="⚠️ Login in first", value="Could not find a Honkai account linked to your Discord ID\nPlease use `/honkai cookies` to set your cookies", inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/vxgLMKG/image.png")
            await ctx.response.send_message(embed=embed, ephemeral=False)
            return
        hashed_ltuid = cookies.get('ltuid')
        hashed_ltoken = cookies.get('ltoken')
        ltuid = decrypt(hashed_ltuid, ctx.author.id)
        ltoken = decrypt(hashed_ltoken, ctx.author.id)
        client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},game=genshin.Game.HONKAI)
        try:
            reward = await client.claim_daily_reward()
        except genshin.AlreadyClaimed:
            # print("Daily reward already claimed")
            signed_in, claimed_rewards = await client.get_reward_info()
            embed = discord.Embed(
                title="Genshin Hoyolab Daily Check-In",
                color=0xFFB6C1,
            )
            embed.add_field(name="✅ Daily Check-In", value="Already checked in today!", inline=False)
            embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/84BtQKB/image.png")
            await ctx.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            if not genshin.AccountNotFound:
                claimed_rewards = await client.get_reward_info()
                embed = discord.Embed(
                    title="Genshin Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                embed.add_field(name="⚠️ Login in first", value="Could not find a Genshin account linked to your Discord ID\nPlease use `/honkai cookies` to set your cookies", inline=False)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                embed.set_thumbnail(url="https://i.ibb.co/vxgLMKG/image.png")
                await ctx.response.send_message(embed=embed, ephemeral=False)
            else:
                embed = discord.Embed(
                    title="Genshin Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                embed.add_field(name="❌ Error", value=f"{e}",inline=False)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                embed.set_thumbnail(url="https://i.ibb.co/ZMhnKcC/Paimon-12.png")
                await ctx.response.send_message(embed=embed, ephemeral=False)
        else:
            # print(f"Claimed {reward.amount}x {reward.name}")
            signed_in, claimed_rewards = await client.get_reward_info()
            embed = discord.Embed(
                title="Genshin Hoyolab Daily Check-In",
                color=0xFFB6C1,
            )
            embed.add_field(name="✅ Collected successfully", value=f"Collected: {reward.amount}x {reward.name}", inline=False)
            embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/9cgyyTG/image.png")
            await ctx.response.send_message(embed=embed, ephemeral=False)
            
    @honkai.command(name="cookies", description="Set cookies for Honkai Impact API requests")
    async def cookies(self, ctx, ltuid: int, ltoken: str):
        hashed_ltuid = encrypt(str(ltuid), ctx.author.id)
        hashed_ltoken = encrypt(ltoken, ctx.author.id)
        Hoyolab_Cookies[ctx.author.id] = {"ltuid": hashed_ltuid, "ltoken": hashed_ltoken}
        embed = discord.Embed(
            title="✅ Hoyolab Cookies",
            description="Cookies set successfully!",
            color=0xFFB6C1,
        )
        embed.set_footer(
            text=f"Requested by {ctx.interaction.user.name} · {datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')}",
            icon_url=ctx.interaction.user.display_avatar.url,
        )
        embed.set_thumbnail(url="https://i.ibb.co/CtfZ02m/image.png")
        await ctx.response.send_message(embed=embed, ephemeral=False)
            
def setup(bot):
    bot.add_cog(HonkaiImpact(bot))