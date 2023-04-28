import discord,typing,os
from discord.colour import Color
from dotenv import load_dotenv
load_dotenv()

def results_embed(database: typing.Optional[str], similarity: typing.Optional[float], author: typing.Optional[str], title: typing.Optional[str], thumbnail: typing.Optional[str]):
    resultsmessage = discord.Embed(
        color=Color.green(),
        title="✅   Sauce Found!",
    )

    if database:
        resultsmessage.add_field(
            name="Database:",
            value=database,
            inline=False
        )

    if similarity:
        sim = f"{similarity}% "
        if similarity >= 95:
            sim = sim + "**(Exact)**"
        elif similarity >= 85.0:
            sim = sim + "**(High)**"
        elif similarity >= 70.0:
            sim = sim + "**(Medium)**"
        elif similarity >= 60.0:
            sim = sim + "**(Low)**"
        else:
            sim = sim + "**(Very Low)**"
               
        resultsmessage.add_field(
            name="Similarity:",
            value=sim,
            inline=False
        )
    if author:
        resultsmessage.add_field(
            name="Author:",
            value=author,
            inline=False
        )

    if title:
        resultsmessage.add_field(
            name="Title:",
            value=title,
            inline=False
        )
    if thumbnail:
        resultsmessage.set_thumbnail(url=thumbnail)
    return resultsmessage

def error_embed(title: str, description: str):
    errormessage = discord.Embed(
        color = Color.red(),
        title = f"❌   {title}",
        description = description
    )
    return errormessage

def help_embed():
    helpmessage = discord.Embed(
        color = Color.nitro_pink(),
        title="🎏   How to use Karin to search images!",
        description=f"""
        Using Karin to search is very easy and straightforward, you only need to say `!saucenao` along with the URL or the file of the anime image. In addition, you can also mention someone to get the source of their profile picture.\n\nThere are aliases to this command, like **"!source", "!sauce", "!sause", "!nao", "!search"**\n\nWhen sending a request, you must use direct image URL. The image must not have unnecessary borders/information, this increases the chances of getting accurate results. Karin only picks results with the similarity of **{float(os.environ.get('SauceNao_MinSimilarity'))}** and above.\n\nPlease do keep in mind that results are not always accurate. To check their accuracy, please refer to the similarity percentage and thumbnail picture.\n\n**Video Demonstration:**        
        """
    ).set_image(
        url = "https://cdn.upload.systems/uploads/kXz4TvKf.gif"
    )
    return helpmessage