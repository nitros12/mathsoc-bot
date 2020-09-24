import random
import ast
import textwrap
import itertools
from typing import List

import discord
from discord import guild
from discord.ext import commands

from mathsoc_bot.utils.checks import is_admin

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def chunk(it, n):
    it = iter(it)
    while True:
        r = list(itertools.islice(it, n))
        if not r:
            break
        yield r

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return is_admin(ctx)

    @commands.command()
    async def mr(self, ctx, *roles: discord.Role):
        """Mention all members that havbe all of the specified roles."""

        if not roles:
            await ctx.send("That would mention everyone")
            return

        roles_s = set(roles)

        to_mention = [m for m in ctx.guild.members if roles_s.issubset(m.roles)]

        pag = commands.Paginator(prefix="", suffix="")

        for line_m in chunk(to_mention, 4):
            pag.add_line(" ".join(m.mention for m in line_m))

        for page in pag.pages:
            await ctx.send(page)

    @commands.command(name="eval")
    async def eval_fn(self, ctx, *, cmd):
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
        - `bot`: the bot instance
        - `discord`: the discord module
        - `commands`: the discord.ext.commands module
        - `ctx`: the invokation context
        - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = textwrap.indent(cmd, " " * 2)

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            "bot": ctx.bot,
            "discord": discord,
            "commands": commands,
            "ctx": ctx,
            "__import__": __import__,
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = await eval(f"{fn_name}()", env)
        await ctx.send(result)
