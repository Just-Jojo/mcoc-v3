from .mcoc import MCOC


def setup(bot):
    bot.add_cog(MCOC(bot))
