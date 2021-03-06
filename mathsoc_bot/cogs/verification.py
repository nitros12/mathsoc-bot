import logging

import discord
from discord.ext import commands

from mathsoc_bot import email_tools
from mathsoc_bot import token_tools
from mathsoc_bot.utils.checks import is_in_mathsoc

logger = logging.getLogger(__name__)


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_member_in_mathsoc(self, user_id: int) -> discord.Member:
        """Try and fetch a member in the mathsoc guild."""
        return self.bot.mathsoc_guild().get_member(user_id)

    def bot_check_once(self, ctx):
        return is_in_mathsoc(ctx)

    @commands.command(name="token")
    async def generate_token(self, ctx, email: email_tools.lancs_email):
        """Generates an authentication token, then emails it to the provided email. You
        must provide a valid lancaster email address or you will not get an
        authentication token.

        """
        auth_token = token_tools.generate_auth_token(ctx.author.id, email)

        logger.info("Generated token for user: %s, %s", ctx.author, auth_token)

        await email_tools.send_verify_email(email, auth_token)

        await ctx.send(f"Okay, I've sent an email to: `{email}` with your token!")

    @commands.command(name="verify")
    async def verify_token(self, ctx, auth_token: str):
        """Takes an authentication token and verifies you.
        Note that tokens expire after 30 minutes.
        """
        user = token_tools.decode_auth_token(auth_token)

        if user is None:
            raise commands.CheckFailure(
                "That token is invalid or is older than 30 minutes and expired."
            )

        user_id, user_email = user

        if user_id != ctx.author.id:
            raise commands.CheckFailure(
                "Seems you're not the same person that generated the token."
            )

        member: discord.Member = self.get_member_in_mathsoc(ctx.author.id)

        assert member is not None

        logger.info("Verifying member: %s", ctx.author)

        await member.add_roles(self.bot.verified_role())

        await ctx.send("Permissions granted, you are now verified!")
        await self.bot.log_message(f"verified member {member} ({member.id}) (email: {user_email})")
