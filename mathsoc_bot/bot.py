import asyncio
import logging
import time

import discord
from discord.ext import commands

from mathsoc_bot import constants
from mathsoc_bot.cogs import admin
from mathsoc_bot.cogs import verification
from mathsoc_bot.cogs import confessions
from mathsoc_bot.secrets import bot_client_token

logger = logging.getLogger(__name__)


class MathsocBot(commands.Bot):
    def __init__(self, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        base_kwargs = {"command_prefix": ["m!"], "pm_help": True, "intents": intents}
        base_kwargs.update(kwargs)
        super().__init__(**base_kwargs)

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Game(name="Prefix: m!")
        )
        print("-----------Bot Credentials-----------")
        print(f"Name:       {self.user.name}")
        print(f"User ID:    {self.user.id}")
        print(f'Timestamp:  {time.strftime("%Y-%m-%d %H:%M:%S")}')
        print("----------------Logs-----------------")

    def run(self, *args, **kwargs):
        self.loop.create_task(self.load_cogs())
        super().run(*args, **kwargs)

    async def load_cogs(self):
        """Register our cogs."""
        await self.wait_until_ready()
        self.add_cog(verification.Verification(self))
        self.add_cog(admin.Admin(self))
        self.add_cog(confessions.Confessions(self))

    def mathsoc_guild(self):
        return self.get_guild(constants.mathsoc_guild_id)

    def verified_role(self):
        return self.mathsoc_guild().get_role(constants.verified_role_id)

    def confession_channel(self):
        return self.mathsoc_guild().get_channel(constants.confession_channel_id)

    async def log_message(self, *args, **kwargs):
        mathsoc_guild = self.mathsoc_guild()
        log_chan = mathsoc_guild.get_channel(constants.bot_log_channel_id)

        if log_chan is None:
            logger.warn("Log channel is missing")
            return

        await log_chan.send(*args, **kwargs)

    async def on_command_error(self, ctx, error):
        # when a command was called invalidly, give info
        if ctx.command is not None:
            cmd = self.help_command.copy()
            cmd.context = ctx
            await cmd.prepare_help_command(ctx, ctx.command.qualified_name)
            prepared_help = cmd.get_command_signature(ctx.command)

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command cannot be used in private messages")
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Command missing required argument: {error}\nUsage: `{prepared_help}`"
            )
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{error}\nUsage: `{prepared_help}`")
            return

        elif isinstance(error, (commands.CommandOnCooldown, commands.CheckFailure)):
            await ctx.send(error)
            return

        elif isinstance(error, commands.CommandNotFound):
            return

        await ctx.send("Something's borked, sorry")
        logger.error(
            "oof: %s", error, exc_info=(type(error), error, error.__traceback__)
        )


def start():
    bot = MathsocBot()
    bot.run(bot_client_token)
