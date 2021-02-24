from redbot.core import commands, Config
from .grab_prestige import grab_prestige
import typing
import discord


class Roster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prestige(self, ctx, champion: str, sig: typing.Optional[str] = "0"):
        """Get a champion's prestige!"""
        # Since right now I'm just testing I don't want a star yet
        # so I'm just gonna use 5* champions
        champion = f"5-{champion}-5"
        data = await grab_prestige(champion, sig)
        embed = discord.Embed(
            title="Champion!", description=data, colour=await ctx.embed_colour()
        )
        await ctx.send(embed=embed)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)
