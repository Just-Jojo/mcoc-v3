import json
import logging
import typing

import aiohttp
import discord
from redbot.core import Config, commands


log = logging.getLogger("red.mcoc-v3/jojo.Roster")


def deci(data: str):
    return data.replace(" ", ".")


class MCOC(commands.Cog):
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

    @commands.command(name="map")
    async def sq_map(self, ctx, quest: deci):
        if not get_map:
            return await ctx.send("Can't do that")
        thing = await get_map(quest=quest)
        if thing is None:
            await ctx.send("Hm, there seems to be an issue with that")
        else:
            (embed := discord.Embed(title=f"Map {quest}")).set_thumbnail(url=thing)
            await ctx.send(embed)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)


################
# MCOC SQ Maps #
################

SQ_URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/images/maps/catmurdock/SQ/{map}.png"


async def get_map(quest: str) -> typing.Union[str, None]:
    quest = f"sq_{quest}"
    async with aiohttp.ClientSession() as session:
        async with session.get((url := SQ_URL.format(map=quest))) as response:
            if response.status == 200:
                ret = url
            else:
                ret = None
    return ret


#######################
# MCOC Prestige Stuff #
#######################

URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/json/backup_prestige.json"
IMAGE_URL = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/images/portraits/{champion}.png"


async def transfer_keys(data: typing.List[dict], look_for: str):
    for item in data:
        key = item.pop("mattkraftid")
        if key == look_for:
            return item
    return "ERROR"


async def grab_prestige(
    champion: str, sig: str, star: str
) -> typing.Tuple[str, typing.Union[None, str]]:
    if not sig.startswith("sig"):
        sig = f"sig{sig}"
    getter = f"{star}-{champion}-{star}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = json.loads(await response.text())
        async with session.get(
            (url := IMAGE_URL.format(champion=champion))
        ) as response:
            log.info(f"{response.status}\n{url}")
            if response.status == 200:
                thumbnail = url
            else:
                thumbnail = None
    if data is None:
        return "ERROR", None
    else:
        grabber = data["rows"]
        data = await transfer_keys(grabber, look_for=getter)
        if data == "ERROR":
            return data, None
        else:
            return data[sig], thumbnail
