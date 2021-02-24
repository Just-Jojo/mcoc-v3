from redbot.core import commands, Config
from . import get_map, grab_prestige
import typing
import discord

import logging

log = logging.getLogger("red.mcoc-v3/jojo.Roster")


def deci(data: str):
    return data.replace(" ", ".")


class Mcoc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def capitalize_all(self, data: str):
        data = data.split(" ")
        return " ".join([x.capitalize() for x in data])

    @commands.command()
    async def prestige(
        self,
        ctx,
        champion: str,
        star: typing.Optional[int] = 5,
        sig: typing.Optional[str] = "0",
    ):
        """Get a champion's prestige!"""
        async with ctx.typing():
            data, thumbnail = await grab_prestige(champion, sig, str(star))
        embed = discord.Embed(
            title=f"{self.capitalize_all(champion)} prestige!",
            description=data,
            colour=await ctx.embed_colour(),
        )
        log.info(thumbnail)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @commands.command()
    async def map(self, ctx, quest: deci):
        thing = await get_map(quest=quest)
        if thing is None:
            await ctx.send("Hm, there seems to be an issue with that")
        else:
            await ctx.send(thing)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)
