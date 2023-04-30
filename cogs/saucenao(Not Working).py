import logging
import typing
import os
import discord
import asyncio

from urllib.request import getproxies
from discord.errors import NotFound
from discord.ext import pages
from discord.ext.pages.pagination import PaginatorButton
from discord.commands import SlashCommandGroup
from discord.ext import commands
from pysaucenao import SauceNao
from pysaucenao.errors import SauceNaoException
from utils import embeds

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

class SauceNao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.saucenao_api_key = os.environ.get("Saucenao_API")
        
    saucenao = SlashCommandGroup("saucenao", "Image search via SauceNao")
    
    @commands.command(name="saucenao", aliases=["source", "sauce", "sause", "nao", "search"])
    async def saucenao(self, ctx, src: typing.Optional[str]):
        resultsPages = []
        results = None
        try:
            if src:
                if src.startswith("<@"):
                    try:
                        member = await self.fetch_user(src.strip("<@!>"))
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
                        member = await self.fetch_user(src)
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
    @commands.message_command(name="Get Image Source")
    async def saucenao(self, ctx: commands.Context, message: discord.Message):
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
                            reaction, user = await self.bot.wait_for(
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
    @commands.user_command(name="Search Avatar Source")
    async def saucenao(self, ctx: commands.Context, member: discord.Member):
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
                            reaction, user = await self.bot.wait_for(
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
    
def setup(bot):
    bot.add_cog(SauceNao(bot))