import nextcord
import random
import os

from googleapiclient.discovery import build
from nextcord.ext import commands
from dotenv.main import load_dotenv

load_dotenv('.env')

class Show(commands.Cog, name="show"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def show(self, ctx, search):   # show picture        
        search = search
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=os.getenv("api_key")).cse()
        result = resource.list(
            q=f"{search}", cx="92f6c5f1da47c499a", searchType="image"        
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = nextcord.Embed(title=f"นี่คือรูป{search}", color=0x84c5e6)

        embed1.set_image(url=url)
        await ctx.send(embed=embed1)
        
def setup(bot:commands.Bot):
    bot.add_cog(Show(bot))