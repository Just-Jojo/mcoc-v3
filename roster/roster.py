from redbot.core import commands, Config
from .grab_prestige import grab_prestige
import typing
import discord

import logging

log = logging.getLogger("red.mcoc-v3/jojo.Roster")


class Roster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            title=f"{champion} prestige!",
            description=data,
            colour=await ctx.embed_colour(),
        )
        log.info(thumbnail)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)
