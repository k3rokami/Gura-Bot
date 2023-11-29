import requests
import re
import json
import discord

from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord import option

class mediadownload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    global BASE_URL,JSON_ENDPOINT,headers,STREAM_ENDPOINT
    
    mediadownload = SlashCommandGroup("mediadownload", "Commands to download media")
    BASE_URL = "https://co.wuk.sh"
    JSON_ENDPOINT = "/api/json"
    STREAM_ENDPOINT = "/api/stream"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    @mediadownload.command(name="twitter", description="Download Twitter Media")
    async def twitter(self, ctx, url: str):
        if 'x.com' in url or 'twitter.com' in url and not 'vxtwitter.com' in url:
            json_request_data = {
                "url": "{}".format(url),
                "filenamePattern": "pretty",
                "vQuality" : "max",
                "aFormat" : "best",
            }
            json_response = requests.post(BASE_URL + JSON_ENDPOINT, json=json_request_data, headers=headers)
            json_data = json_response.json()
            error = json_data.get("text", "")
            status = json_data.get("status", "")
            cobalt_url = json_data.get("url", "")
            if error:
                pattern = r'/status/(\d+)\??'
                match1 = re.search(pattern, url)
                match2 = re.search(pattern, url)
                if match1:
                    status_number = match1.group(1)
                elif match2:
                    status_number = match2.group(1)
                response = requests.get(f"https://api.vxtwitter.com/Twitter/status/{status_number}")
                tweet = json.loads(response.text)
                media_url = tweet.get("mediaURLs", [])
                tweet_url = tweet.get("tweetURL", "")
                url_pattern = r'https:\/\/t\.co\/\w+'
                text_original = tweet.get("text", "")
                text = re.sub(url_pattern, '', text_original)
                likes = tweet.get("likes", "")
                user_name = tweet.get("user_name", "")
                user_screen_name = tweet.get("user_screen_name", "")
                for media in media_url:
                    await ctx.send(media)
                print(tweet)
            elif "rate-limit" in status:
                await ctx.send("Rate Limit Exceeded", ephemeral=True)
            else:
                await ctx.send(cobalt_url)
    
    @mediadownload.command(name="youtube", description="Download YouTube Media")
    @option("vcodec",
            description="Select the codec from the list",
            choices=["h264","av1","vp9"],
            required=False)
    @option("vquality",
            description="Select the video quality from the list",
            choices=["140","240","720","1080","2160","max"],
            required=False)
    @option("aformat",
            description="Select the audio quality from the list",
            choices=["mp3","ogg","wav","opus","best"],
            required=False)
    @option("--isaudioonly", description="Only Audio", type=bool, default=False)
    async def YouTube(self, ctx, url: str, vcodec:str = "h264", vquality: str = "max", aformat:str = "mp3", isaudioonly: bool = False):
        json_request_data = {
            "url": "{}".format(url),
            "filenamePattern": "pretty",
            "vCodec" : "{}".format(vcodec),
            "vQuality" : "{}".format(vquality),
            "aFormat" : "{}".format(aformat),
        }
        json_response = requests.post(BASE_URL + JSON_ENDPOINT, json=json_request_data, headers=headers)
        json_data = json_response.json()
        print(json_data)
        cobalt_url = json_data.get("url", "")
        status = json_data.get("status", "")
        if "rate-limit" in status:
            await ctx.send("Rate Limit Exceeded", ephemeral=True)
        elif "error" in status:
            error = json_data.get("text", "")
            await ctx.send(f"Error: {error}", ephemeral=True)
        else:
            await ctx.send(cobalt_url)
    
    @mediadownload.command(name="tiktok", description="Download TikTok Media")
    @option("vquality",
            description="Select the video quality from the list",
            choices=["140","240","720","1080","2160","max"],
            required=False)
    @option("--isnottwatermark", description="Remove TikTok watermark from video", type=bool, default=True)
    @option("--isttfullaudio", description="Downloads the original music used", type=bool, default=False)
    async def TikTok(self, ctx, url: str, vquality: str = "max",  isttfullaudio: bool = False, isnottwatermark: bool = True):
        json_request_data = {
            "url": "{}".format(url),
            "filenamePattern": "pretty",
            "vQuality" : "{}".format(vquality),
            "isTTFullAudio" : "{}".format(isttfullaudio),
            "isNoTTWatermark" : "{}".format(isnottwatermark)
        }
        json_response = requests.post(BASE_URL + JSON_ENDPOINT, json=json_request_data, headers=headers)
        json_data = json_response.json()
        print(json_data)
        cobalt_url = json_data.get("url", "")
        status = json_data.get("status", "")
        if "rate-limit" in status:
            await ctx.send("Rate Limit Exceeded", ephemeral=True)
        elif "error" in status:
            error = json_data.get("text", "")
            await ctx.send(f"Error: {error}", ephemeral=True)
        else:
            await ctx.send(cobalt_url)
            
    @mediadownload.command(name="download", description="Download Media from Bilibili,Instagram,Reddit etc.")
    @option("vquality",
            description="Select the video quality from the list",
            choices=["140","240","720","1080","2160","max"],
            required=False)
    @option("aformat",
            description="Select the audio quality from the list",
            choices=["mp3","ogg","wav","opus","best"],
            required=False)
    @option("--isaudioonly", description="Only Audio", type=bool, default=False)
    async def YouTube(self, ctx, url: str, vquality: str = "max", aformat:str = "mp3", isaudioonly: bool = False):
        json_request_data = {
            "url": "{}".format(url),
            "filenamePattern": "pretty",
            "vQuality" : "{}".format(vquality),
            "aFormat" : "{}".format(aformat),
        }
        json_response = requests.post(BASE_URL + JSON_ENDPOINT, json=json_request_data, headers=headers)
        json_data = json_response.json()
        print(json_data)
        cobalt_url = json_data.get("url", "")
        status = json_data.get("status", "")
        if "rate-limit" in status:
            await ctx.send("Rate Limit Exceeded", ephemeral=True)
        elif "error" in status:
            error = json_data.get("text", "")
            await ctx.send(f"Error: {error}", ephemeral=True)
        else:
            await ctx.send(cobalt_url)
            
def setup(bot):
    bot.add_cog(mediadownload(bot))