import discord
from discord.abc import GuildChannel
import requests
import aiohttp
import typing

import logging


log = logging.getLogger("red.mcoc-v3.Embed")


class CDTEmbed:
    """CollectorDevTeam basic Embed creator

    Attributes
    ----------
    bot: :class:`Red`
        The bot for grabbing defaults from
    default_member_color: :class:`str`
        A string to match against a member's color
    """

    def __init__(self, bot):
        self.default_member_color = "#000000"
        self.bot = bot

    async def create(
        self,
        ctx,
        color=discord.Color.gold(),
        title="",
        description="",
        image=None,
        thumbnail=None,
        url=None,
        footer_text=None,
        footer_url=None,
        author_text=None,
    ):
        """Return a color styled embed with CDT footer, and optional title or description.
        user_id = user id string. If none provided, takes message author.
        color = manual override, otherwise takes gold for private channels, or author color for guild.
        title = String, sets title.
        description = String, sets description.
        image = String url.  Validator checks for valid url.
        thumbnail = String url. Validator checks for valid url."""
        COLLECTOR_ICON = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/cdt_icon.png"
        PATREON = "https://patreon.com/collectorbot"
        CDT_LOGO = "https://raw.githubusercontent.com/CollectorDevTeam/assets/master/data/cdt_logo.png"

        if isinstance(ctx.channel, GuildChannel):
            if (acolor := ctx.author.color) is not self.default_member_color:
                color = acolor
            else:
                color = color
        if url is None:
            url = PATREON
        data = discord.Embed(color=color, title=title, url=url)
        if description is not None:
            if len(description) < 1500:
                data.description = description
        data.set_author(
            name=ctx.author.display_name, icon_url=ctx.message.author.avatar_url
        )
        if image is not None:
            status = await self.get_status_code(url=image)
            if status == 200:
                data.set_image(url=image)
            else:
                log.error(
                    (f"Image URL Failure, code {status}" f"\nAttempted URL:\n{image}")
                )
        if thumbnail is None:
            thumbnail = CDT_LOGO
        else:
            status = await self.get_status_code(url=thumbnail)
            if status == 200:
                data.set_thumbnail(url=thumbnail)
            else:
                data.set_thumbnail(url=CDT_LOGO)
                log.error(
                    (
                        f"Thumbnail URL Failure, code {status}"
                        f"\nAttempted URL:\n{thumbnail}"
                    )
                )
        if footer_text is None:
            footer_text = "Collector | Contest of Champions | CollectorDevTeam"
        if footer_url is None:
            footer_url = CDT_LOGO
        data.set_footer(text=footer_text, icon_url=footer_url)
        return data

    async def get_status_code(self, url: str) -> typing.List[int]:
        client = aiohttp.ClientSession()
        async with client.get(url) as response:
            ret = response.status
        await client.close()
        return ret
