from discord.commands import SlashCommandGroup
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    Edit = SlashCommandGroup("edit", "Various help commands for Gura!")
    
def setup(bot):
    bot.add_cog(MyCog(bot))