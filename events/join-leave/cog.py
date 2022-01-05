import nextcord
import os

from dotenv import load_dotenv
from nextcord.ext import commands

load_dotenv('.env')

welcome_room = int(os.getenv("WELROOM"))

class Events(commands.Cog, name="events"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed=nextcord.Embed(description=f"{member.name} has joined." , color=0x2ECC71)
        await self.bot.get_channel(welcome_room).send(embed = embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed=nextcord.Embed(description=f"{member.name} has leaved." , color=0xC70039)
        await self.bot.get_channel(welcome_room).send(embed = embed)
    
def setup(bot:commands.Bot):
    bot.add_cog(Events(bot))