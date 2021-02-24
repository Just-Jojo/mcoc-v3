import discord
from redbot.core import commands, checks
from redbot.core.config import Config
from redbot.core.utils import menus, chat_formatting
from .cdtembed import CDTEmbed
import random
import asyncio

_guild_ids = (215271081517383682, 378035654736609280)
_collector = "https://images-ext-1.discordapp.net/external/6Q7QyBwbwH2SCmwdt_YR_ywkHWugnXkMc3rlGLUnvCQ/https/raw.githubusercontent.com/CollectorDevTeam/assets/master/data/images/featured/collector.png?width=230&height=230"


class CdtCommon(commands.Cog):
    """
    Common Files
    """

    def __init__(self, bot):
        self.bot = bot
        self.cdtguild = self.bot.get_guild(215271081517383682)
        self.Embed = Embed(self)
        self.config = Config.get_conf(
            self,
            identifier=8675309,
            force_registration=True,
        )

    @commands.command(name="promote", aliases=("promo",))
    @cst_check()
    async def cdt_promote(self, ctx, channel: discord.TextChannel, *, content):
        """Content will fill the embed description.
        title;content will split the message into Title and Content.
        An image attachment added to this command will replace the image embed."""
        authorized = self.check_collectorsupportteam(ctx)
        if authorized is not True:
            return
        else:
            pages = []
            if len(ctx.message.attachments) > 0:
                image = ctx.message.attachments[0]
                imgurl = image.url
            else:
                imagelist = [
                    "https://cdn.discordapp.com/attachments/391330316662341632/725045045794832424/collector_dadjokes.png",
                    "https://cdn.discordapp.com/attachments/391330316662341632/725054700457689210/dadjokes2.png",
                    "https://cdn.discordapp.com/attachments/391330316662341632/725055822023098398/dadjokes3.png",
                    "https://cdn.discordapp.com/attachments/391330316662341632/725056025404637214/dadjokes4.png",
                    "https://media.discordapp.net/attachments/391330316662341632/727598814327865364/D1F5DE64D72C52880F61DBD6B2142BC6C096520D.png",
                    "https://media.discordapp.net/attachments/391330316662341632/727598813820485693/8952A192395C772767ED1135A644B3E3511950BA.jpg",
                    "https://media.discordapp.net/attachments/391330316662341632/727598813447192616/D77D9C96DC5CBFE07860B6211A2E32448B3E3374.jpg",
                    "https://media.discordapp.net/attachments/391330316662341632/727598812746612806/9C15810315010F5940556E48A54C831529A35016.jpg",
                ]
                imgurl = random.choice(imagelist)
            data = await self.Embed.create(
                ctx,
                title="CollectorVerse Tips:sparkles:",
                description=content,
                image=imgurl,
            )
            data.set_author(
                name="{} of CollectorDevTeam".format(ctx.author.display_name),
                icon_url=ctx.author.avatar_url,
            )
            data.add_field(
                name="Alliance Template",
                value="[Make an Alliance Guild](https://discord.new/gtzuXHq2kCg4)\nRoles, Channels & Permissions pre-defined",
                inline=False,
            )
            data.add_field(
                name="Get Collector",
                value="[Invite](https://discord.com/oauth2/authorize?client_id=210480249870352385&scope=bot&permissions=8)",
                inline=False,
            )
            data.add_field(
                name="Support",
                value="[CollectorDevTeam Guild](https://discord.gg/BwhgZxk)",
                inline=False,
            )
            await channel.send(embed=data)

    @commands.command()
    @commands.guild_only()
    async def showtopic(self, ctx, channel: discord.TextChannel = None):
        """Show the Channel Topic in the chat channel as a CDT Embed."""
        if channel is None:
            channel = ctx.message.channel
        topic = channel.topic
        if topic is not None and topic != "":
            data = await self.Embed.create(
                ctx,
                title="#{} Topic :sparkles:".format(channel.name),
                description=topic,
            )
            data.set_thumbnail(url=ctx.message.guild.icon_url)
            await ctx.send(embed=data)

    @commands.command(name="list_members", aliases=("list_users", "rr"))
    async def _users_by_role(self, ctx, role: discord.Role, use_alias=True):
        """Embed a list of server users by Role"""
        guild = ctx.message.guild
        pages = []
        members = await self._list_users(ctx, role, ctx.guild)
        if members is not None:
            if use_alias is True:
                ret = "\n".join("{0.display_name}".format(m) for m in members)
            else:
                ret = "\n".join("{0.name} [{0.id}]".format(m) for m in members)
            # pagified = chat_formatting.pagify(ret)
            for page in chat_formatting.pagify(ret):
                data = await self.Embed.create(
                    ctx,
                    title="{0.name} Role - {1} member(s)".format(role, len(members)),
                    description=page,
                )
                pages.append(data)
            if len(pages) == 1:
                await ctx.send(embed=data)
            else:
                asyncio.create_task(menus.menu(ctx, pages, menus.DEFAULT_CONTROLS))

    # If a list is too large it will start blocking the bot
    # Making this a corotuine helps prevent that a bit
    async def _list_users(self, ctx, role: discord.Role, guild: discord.guild):
        """Given guild and role, return member list"""
        members = []
        for member in guild.members:
            if role in member.roles:
                members.append(member)
        if len(members) > 0:
            return members
        else:
            return None

    ### Static methods

    @staticmethod
    def from_flat(flat, ch_rating):
        """Get a numbe from a flat"""
        denom = 5 * ch_rating + 1500 + flat
        return round(100 * flat / denom, 2)

    @staticmethod
    def to_flat(per, ch_rating):
        """Transform a number to a flat"""
        num = (5 * ch_rating + 1500) * per
        return round(num / (100 - per), 2)


def cdt_check():
    async def pred(ctx: commands.Context):
        return check_collectordevteam(guild=ctx.guild, author=ctx.author)

    return commands.check(pred)


def cst_check():
    """Check for CollectorSupportTeam"""

    async def pred(ctx: commands.Context):
        guild = ctx.guild
        author = ctx.author

        if guild.id not in _guild_ids:
            return False
        if check_collectordevteam(guild, author):
            # Let CDT members use CST commands
            return True
        if guild.id == _guild_ids[1]:
            role = guild.get_role(727582658678358136)
        else:
            role = guild.get_role(390253719125622807)
        return role in author.roles

    return commands.check(pred)


def check_collectordevteam(guild: discord.Guild, author: discord.Member) -> bool:
    if guild.id not in _guild_ids:
        return False
    if guild.id == _guild_ids[1]:
        # UMCOC
        role = guild.get_role(399779614555373580)
    else:
        # CollectorDevTeam
        role = guild.get_role(390253643330355200)
    return role in author.roles


def umcoc():
    async def pred(ctx: commands.Context):
        return ctx.guild.id == _guild_ids[1]

    return commands.check(pred)


def cdt():
    async def pred(ctx: commands.Context):
        return ctx.guild.id == _guild_ids[0]

    return commands.check(pred)
