import genshin
import discord
import datetime
import requests
import json
import pytz

from typing import Optional
from cogs.genshin import encrypt,decrypt,sgt_time
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
            embed.add_field(name="⚠️ Login first", value="Could not find a Honkai account linked to your Discord ID\nPlease use `/honkai cookies` to set your cookies", inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/vxgLMKG/image.png")
            await ctx.response.send_message(embed=embed, ephemeral=False)
            return
        hashed_ltuid = cookies.get('ltuid')
        hashed_ltoken = cookies.get('ltoken')
        ltuid = decrypt(hashed_ltuid, ctx.author.id)
        ltoken = decrypt(hashed_ltoken, ctx.author.id)
        language = cookies.get('language')
        client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken},lang=language,game=genshin.Game.HONKAI)
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
            if language == "ja-jp":
                japanese_embed = discord.Embed(
                    title="崩壊3rd 今日のログインボーナス",
                    color=0xFFB6C1,
                )
                japanese_embed.add_field(name="✅ デイリーチェックイン", value="今日はすでにチェックインしました！", inline=False)
                japanese_embed.add_field(name="今月の獲得報酬の合計：", value=claimed_rewards)
                japanese_embed.set_footer(
                    text=f"{ctx.interaction.user.name} さんによってリクエストされました · {sgt_time}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                japanese_embed.set_thumbnail(url="https://i.ibb.co/84BtQKB/image_ja.png")
                embed = japanese_embed
            else:
                embed = discord.Embed(
                    title="Honkai Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                embed.add_field(name="✅ Daily Check-In", value="Already checked in today!", inline=False)
                embed.add_field(name="Total claimed rewards this month:", value=claimed_rewards)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                embed.set_thumbnail(url="https://i.ibb.co/84BtQKB/image.png")
            await ctx.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            if not genshin.AccountNotFound:
                claimed_rewards = await client.get_reward_info()
                if language == "ja-jp":
                    embed = discord.Embed(
                    title="崩壊3rd 今日のログインボーナス",
                    color=0xFFB6C1,
                )
                    embed.add_field(name="⚠️ ログインしてください", value="あなたのDiscord IDにリンクされた原神アカウントが見つかりませんでした。\n`/honkai cookies`を使用してクッキーを設定してください。", inline=False)
                else:
                    embed = discord.Embed(
                    title="Honkai Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                    embed.add_field(name="⚠️ Login first", value="Could not find a Genshin account linked to your Discord ID\nPlease use `/honkai cookies` to set your cookies", inline=False)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
                    icon_url=ctx.interaction.user.display_avatar.url,
                )
                embed.set_thumbnail(url="https://i.ibb.co/vxgLMKG/image.png")
                await ctx.response.send_message(embed=embed, ephemeral=False)
            else:
                if language == "ja-jp":
                    embed = discord.Embed(
                    title="崩壊3rd 今日のログインボーナス",
                    color=0xFFB6C1,
                )
                    embed.add_field(name="❌ エラー", value=f"{e}",inline=False)
                else:
                    embed = discord.Embed(
                    title="Honkai Hoyolab Daily Check-In",
                    color=0xFFB6C1,
                )
                    embed.add_field(name="❌ Error", value=f"{e}",inline=False)
                embed.set_footer(
                    text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
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
                text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
                icon_url=ctx.interaction.user.display_avatar.url,
            )
            embed.set_thumbnail(url="https://i.ibb.co/9cgyyTG/image.png")
            if language == "ja-jp":
                embed = discord.Embed(
                title="崩壊3rd 今日のログインボーナス",
                color=0xFFB6C1,
            )
                embed.add_field(name="✅ 取得成功", value=f"取得：{reward.amount}x {reward.name}", inline=False)
                embed.add_field(name="今月の獲得報酬の合計：", value=claimed_rewards)
            await ctx.response.send_message(embed=embed, ephemeral=False)
            
    @honkai.command(name="cookies", description="Set cookies for Honkai Impact API requests")
    @option("language",
            description="Enter the redemption code or choose from the list.",
            choices=["English", "日本語", "한국어", "简体中文", "繁體中文", "Indonesia", "Deutsch", "Español", "Français", "Français", "Português", "Pусский", "ภาษาไทย", "Tiếng Việt"],
            required=True)
    async def cookies(self, ctx, ltuid: int, ltoken: str, cookie_token: str, language: str):
        hashed_ltuid = encrypt(str(ltuid), ctx.author.id)
        hashed_ltoken = encrypt(ltoken, ctx.author.id)
        hashed_cookie_token = encrypt(str(cookie_token), ctx.author.id)
        if language == "English":
            lang = "en-us"
        elif language == "日本語":
            lang = "ja-jp"
        elif language == "简体中文":
            lang = "zh-cn"
        elif language == "繁體中文":
            lang = "zh-tw"
        elif language == "Deutsch":
            lang = "id-id"
        elif language == "Indonesia":
            lang = "de-de"
        elif language == "Español":
            lang = "es-es"
        elif language == "Français":
            lang = "fr-fr"
        elif language == "Português":
            lang = "pt-pt"
        elif language == "Pусский":
            lang = "ru-ru"
        elif language == "ภาษาไทย":
            lang = "th-th"
        elif language == "Tiếng Việt":
            lang = "vi-vn"
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
            Hoyolab_Cookies[str(ctx.author.id)]["language"]  = lang
        else:
            # Create a new entry
            Hoyolab_Cookies[str(ctx.author.id)] = {"ltuid": hashed_ltuid, "ltoken": hashed_ltoken, "cookie_token": hashed_cookie_token, "language": lang, "genshin_auto": False, "honkai_auto": False}
        with open('Hoyolab_Cookies.json', 'w') as f:
            json.dump(Hoyolab_Cookies, f)
        embed = discord.Embed(
            title="✅ Hoyolab Cookies",
            description="Cookies set successfully!",
            color=0xFFB6C1,
        )
        if language == "日本語":
            embed = discord.Embed(
                title="✅ Hoyolab クッキー",
                description="クッキーが正常に設定されました！",
                color=0xFFB6C1,
            )
        embed.set_footer(
            text=f"Requested by {ctx.interaction.user.name} · {sgt_time}",
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