import random

from .cdtembed import CDTEmbed
import json
import aiohttp
import discord
from redbot.core import commands, checks
from redbot.core.config import Config


class DadJokes(commands.Cog):
    """Random dad jokes from icanhazdadjoke.com"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=949000000949,
            force_registration=True,
        )
        self.channel = self.bot.get_channel("725065939460030575")
        self.Embed = Embed(self.bot)
        # self.diagnostics = DIAGNOSTICS(self.bot)
        self.dadjoke_images = [
            "https://cdn.discordapp.com/attachments/391330316662341632/725045045794832424/collector_dadjokes.png",
            "https://cdn.discordapp.com/attachments/391330316662341632/725054700457689210/dadjokes2.png",
            "https://cdn.discordapp.com/attachments/391330316662341632/725055822023098398/dadjokes3.png",
            "https://cdn.discordapp.com/attachments/391330316662341632/725056025404637214/dadjokes4.png",
        ]

    @commands.command(
        pass_context=True,
        aliases=(
            "joke",
            "dadjokes",
            "jokes",
        ),
    )
    async def dadjoke(self, ctx):
        """Gets a random dad joke."""
        author = ctx.author
        joke = await self.get_joke()
        data = self.Embed.create(
            ctx, title="CollectorVerse Dad Jokes:sparkles:", description=joke
        )
        data.set_author
        data.set_image(url=random.choice(self.dadjoke_images))
        await ctx.send(embed=data)

    async def get_joke(self):
        api = "https://icanhazdadjoke.com/slack"
        joke = None
        while joke is None:
            async with aiohttp.ClientSession() as session:
                async with session.get(api) as response:
                    result = await response.json()
                    attachments = result["attachments"][0]
                    joke = attachments["text"]
        return joke
