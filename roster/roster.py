from redbot.core import commands, Config
from .grab_prestige import grab_prestige
import typing
import discord


class Roster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prestige(
        self,
        ctx,
        champion: str,
        sig: typing.Optional[str] = "0",
        star: typing.Optional[str] = "5",
    ):
        """Get a champion's prestige!"""
        champion = f"{star}-{champion}-{star}"
        async with ctx.typing():
            data = await grab_prestige(champion, sig)
        embed = discord.Embed(
            title="Champion!", description=data, colour=await ctx.embed_colour()
        )
        await ctx.send(embed=embed)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)
