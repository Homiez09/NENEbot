import nextcord
from nextcord.ext import commands

class Say(commands.Cog, name="say"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.command() 
    @commands.has_guild_permissions(administrator=True)
    async def say(self, ctx,* ,message):
        embed = nextcord.Embed(description = message, color=0x2ECC71)
        await ctx.channel.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Say(bot))