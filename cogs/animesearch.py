import kadal
import discord 

from kadal import MediaNotFound
from discord.ext import commands

klient = kadal.Client()

AL_ICON = "https://avatars2.githubusercontent.com/u/18018524?s=280&v=4"

class AnimeMangaSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # ALanime = SlashCommandGroup("alanime", "Searches anime using AniList")
    # ALmanga = SlashCommandGroup("almanga", "Searches manga using AniList")
    
    @commands.slash_command(name="anime", description="Gura helps you to search anime using AniList")
    async def al_anime(self, interaction, *, name):
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


    @commands.slash_command(name="manga", description="Gura helps you to search manga using AniList")
    async def al_manga(self, interaction, *, name):
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
        
def setup(bot):
    bot.add_cog(AnimeMangaSearch(bot))