import logging
from datetime import datetime

import discord
from discord.ext import commands

from mathsoc_bot.utils.checks import is_in_mathsoc

logger = logging.getLogger(__name__)


class Confessions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def bot_check_once(self, ctx):
        return is_in_mathsoc(ctx)

    @commands.command(name="confess")
    async def command(self, ctx, *, confession: str):
        """Confess to your sins."""
        confession = confession.strip()

        if not confession:
            await ctx.send("You have nothing to confess?")
            return

        warn_dm_message = ""

        if ctx.guild:
            await ctx.message.delete()
            warn_dm_message = "\n\nP.S. Keep this in DMs next time."

        embed = discord.Embed(
            description=confession,
            timestamp=datetime.now(),
            color=discord.Colour.dark_teal(),
        )
        embed.set_author(name="Anonymous")

        await self.bot.confession_channel().send(embed=embed)

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url_as(format="png"),
        )

        embed.title = "A confession"

        await self.bot.log_message(embed=embed)

        await ctx.send("Ego te absolvo" + warn_dm_message)
