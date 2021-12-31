import nextcord
from nextcord.ext import commands

class Move(commands.Cog, name="move"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def move(self, ctx, channel : nextcord.VoiceChannel):
        try:    
            for members in ctx.author.voice.channel.members:
                embed = nextcord.Embed(description=f'Move {members} to {channel}', color=0x2ECC71)
                await members.move_to(channel)
                await ctx.send(embed = embed)
        except:
            embed = nextcord.Embed(description='Something Went Wrong!!', color=0xC70039)
            await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Move(bot))