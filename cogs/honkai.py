import genshin
import discord
import datetime
import requests
import json

from typing import Optional
from cogs.genshin import encrypt,decrypt
from cogs.hoyolab import Hoyolab_Cookies
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import option

class HonkaiImpact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    honkai = SlashCommandGroup("honkai", "Various Hoyolab Honkai Impact Commands")
    
    @honkai.command(name="daily", description="Receive Hoyolab daily check-in reward")
    @option("--auto-claim", type=bool, default=False, description="Automatically claim the daily reward")
    async def daily(self, ctx, auto_claim: Optional[bool] = False):
        with open("Hoyolab_Cookies.json", 'r') as f:
            Hoyolab_Cookies = json.load(f)
            cookies = Hoyolab_Cookies.get(str(ctx.author.id))
        if cookies == None:
            embed = discord.Embed(
                title="Honkai Hoyolab Daily Check-In",
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
            if auto_claim:
                Hoyolab_Cookies[str(ctx.author.id)]['honkai_auto'] = True
                with open("Hoyolab_Cookies.json", 'w') as f:
                    json.dump(Hoyolab_Cookies, f, indent=4)
                reward = await client.claim_daily_reward()
            else:
                reward = await client.claim_daily_reward()
        except genshin.AlreadyClaimed:
            # print("Daily reward already claimed")
            signed_in, claimed_rewards = await client.get_reward_info()
            embed = discord.Embed(
                title="Honkai Hoyolab Daily Check-In",
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
                    title="Honkai Hoyolab Daily Check-In",
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
                    title="Honkai Hoyolab Daily Check-In",
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
                title="Honkai Hoyolab Daily Check-In",
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
    async def cookies(self, ctx, ltuid: int, ltoken: str, cookie_token: str):
        hashed_ltuid = encrypt(str(ltuid), ctx.author.id)
        hashed_ltoken = encrypt(ltoken, ctx.author.id)
        hashed_cookie_token = encrypt(str(cookie_token), ctx.author.id)
        try:
            with open('Hoyolab_Cookies.json', 'r') as f:
                Hoyolab_Cookies = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Create a new dictionary if the file does not exist or is empty
            Hoyolab_Cookies = {}
        if str(ctx.author.id) in Hoyolab_Cookies:
            # Update the existing values
            Hoyolab_Cookies[str(ctx.author.id)]["ltuid"] = hashed_ltuid
            Hoyolab_Cookies[str(ctx.author.id)]["ltoken"] = hashed_ltoken
            Hoyolab_Cookies[str(ctx.author.id)]["cookie_token"] = hashed_cookie_token
        else:
            # Create a new entry
            Hoyolab_Cookies[str(ctx.author.id)] = {"ltuid": hashed_ltuid, "ltoken": hashed_ltoken, "cookie_token": hashed_cookie_token, "genshin_auto": False, "honkai_auto": False}
        with open('Hoyolab_Cookies.json', 'w') as f:
            json.dump(Hoyolab_Cookies, f)
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
    
    if requests.get("https://honkai-redeem-code.vercel.app/codes").status_code == 200:
        data = requests.get("https://honkai-redeem-code.vercel.app/codes").json()
        codes = [code['code'] for code in data]
    else:
        print("Failed to retrieve data from server.")

    @honkai.command(name="codes", description="Redeem Genshin Codes")
    @option("code",
            description="Enter the redemption code or choose from the list.",
            choices=codes,
            required=False)
    async def codes(self, ctx, code: str = None):
        with open("Hoyolab_Cookies.json", 'r') as f:
            Hoyolab_Cookies = json.load(f)
            cookies = Hoyolab_Cookies.get(str(ctx.author.id))
        if cookies == None:
            await ctx.respond(f"Cookies are not set for {ctx.author}. Please set cookies with '/genshin cookies'", ephemeral=False)
            return
        hashed_ltuid = cookies.get('ltuid')
        hashed_ltoken = cookies.get('ltoken')
        hashed_cookie_token = cookies.get('cookie_token')
        ltuid = decrypt(hashed_ltuid, ctx.author.id)
        ltoken = decrypt(hashed_ltoken, ctx.author.id)
        cookie_token = decrypt(hashed_cookie_token, ctx.author.id)
        client = genshin.Client(cookies={"ltuid": ltuid, "ltoken": ltoken,"account_id": ltuid,"cookie_token": cookie_token})
        try:
            await client.redeem_code(code,uid=await client._get_uid(game=genshin.Game.HONKAI))
            embed = discord.Embed(
                title="Genshin Redeemption Code",
                color=0xFFB6C1,
            )
            embed.add_field(name="Redemption Successful:", value=f"You have successfully redeemed code: {code}",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/QcsQ6K0/Klee-1.png")
            await ctx.send(embed=embed)
            
        except genshin.RedemptionInvalid:
            embed = discord.Embed(
                title="Genshin Redeemption Code",
                color=0xFFB6C1,
            )
            embed.add_field(name="Redemption Code Invalid:", value="Current redemption code is invalid.",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/F46d03S/image.png")
            await ctx.send(embed=embed)
            
        except genshin.RedemptionCooldown:
            embed = discord.Embed(
                title="Genshin Redeemption Code",
                color=0xFFB6C1,
            )
            embed.add_field(name="Redemption Code Cooldown:", value="You're redeeming too fast! Please try again later.",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/YWKvYvp/Klee-2.png")
            await ctx.send(embed=embed)
            
        except genshin.RedemptionClaimed:
            embed = discord.Embed(
                title="Genshin Redeemption Code",
                color=0xFFB6C1,
            )
            embed.add_field(name="Redemption Code Claimed:", value="Current redemption code has been claimed already.",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/mFRNHjT/image.png")
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title="Genshin Redeemption Code",
                color=0xFFB6C1,
            )
            embed.add_field(name="An error has occured:", value=f"{e}",inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/hc0KzPX/image.png")
            await ctx.send(embed=embed)
            print(f"An exception occurred: {e}")
            
def setup(bot):
    bot.add_cog(HonkaiImpact(bot))