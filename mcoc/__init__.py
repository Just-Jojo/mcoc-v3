from .mcoc import Mcoc


def setup(bot):
    bot.add_cog(Mcoc(bot))
