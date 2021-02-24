from .roster import Roster


def setup(bot):
    bot.add_cog(Roster(bot))
