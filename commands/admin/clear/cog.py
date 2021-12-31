from nextcord.ext import commands
        
class Clear(commands.Cog, name="Clear"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command() # clear
    @commands.has_guild_permissions(administrator=True)
    async def clear(self, ctx: commands.Context, limit=5):
        await ctx.channel.purge(limit=limit+1)
    
def setup(bot:commands.Bot):
    bot.add_cog(Clear(bot))