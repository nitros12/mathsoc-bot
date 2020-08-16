import discord
from discord.ext import commands

from mathsoc_bot.constants import mathsoc_guild_id
from mathsoc_bot.db.models import User


def in_channel(channel_id: int):
    def inner(ctx: commands.Context):
        if ctx.channel.id != channel_id:
            raise commands.CheckFailure(
                f"This command is only usable inside <#{channel_id}>"
            )
        return True

    return inner


def is_in_mathsoc(ctx: commands.Context) -> bool:
    """Ensure a member is in the mathsoc guild."""
    if ctx.bot.mathsoc_guild().get_member(ctx.author.id) is None:
        raise commands.CheckFailure(
            "It looks like you're not in the mathsoc guild?"
        )

    return True


def is_admin(ctx: commands.Context) -> bool:
    """Ensure a member is an admin."""
    member_in_mathsoc = ctx.bot.get_guild(mathsoc_guild_id).get_member(ctx.author.id)
    if member_in_mathsoc is None:
        raise commands.CheckFailure(
            "You must be an admin in mathsoc to use this command.."
        )

    is_admin = member_in_mathsoc.guild_permissions.administrator

    if not is_admin:
        raise commands.CheckFailure(
            "You must be an admin to use this command."
        )

    return True


async def is_authed(ctx: commands.Context) -> bool:
    """Ensure a member is registered with Mathsoc."""

    user = await User.get(ctx.author.id)

    if user is None:
        raise commands.CheckFailure(
            "It looks like you're not registed with mathsoc, go and register yourself."
        )

    return True
