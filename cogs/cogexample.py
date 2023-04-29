from discord.commands import SlashCommandGroup
from discord.ext import commands
import discord

class MyCog(commands.Cog):
    def __init__(self, bot_: discord.Bot):
        self.bot = bot_

    greetings = SlashCommandGroup("greetings", "Various greeting from cogs!")

    international_greetings = greetings.create_subgroup(
        "international", "International greetings"
    )

    secret_greetings = SlashCommandGroup(
        "secret_greetings",
        "Secret greetings",
        checks=[
            commands.is_owner().predicate
        ],  # Ensures the owner_id user can access this group, and no one else
    )

    @greetings.command()
    async def greetings(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hello, this is a slash subcommand from a cog!")

    @greetings.command(name="international_test")
    async def aloha(self, ctx: discord.ApplicationContext):
        await ctx.respond("Aloha, a Hawaiian greeting")

    @secret_greetings.command()
    async def secret_handshake(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        await ctx.respond(f"{member.mention} secret handshakes you")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        if isinstance(error, commands.NotOwner):
            await ctx.respond("You can't use that command!")
        else:
            raise error  # Raise other errors so they aren't ignored
