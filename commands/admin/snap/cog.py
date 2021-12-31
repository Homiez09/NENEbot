import nextcord
from nextcord.ext import commands

class Snap(commands.Cog, name="snap"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def snap(self, ctx):
        try:    
            await ctx.send("https://cdn.discordapp.com/attachments/875313424601612318/925727431644561499/Thanos.gif")
            for members in ctx.author.voice.channel.members:
                await members.move_to(None)
                await ctx.send(f"{members.mention} was slain by Thanos, for the good of the Universe.")
        except:
            embed = nextcord.Embed(description='Something Went Wrong!!', color=0xC70039)
            await ctx.send(embed=embed)
            
def setup(bot:commands.Bot):
    bot.add_cog(Snap(bot))    