from .mcoc import Mcoc
from .maps import get_map
from .grab_prestige import grab_prestige


def setup(bot):
    bot.add_cog(Mcoc(bot))
