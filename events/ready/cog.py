import nextcord
import os

from dotenv import load_dotenv
from nextcord.ext import commands
from datetime import datetime as date

load_dotenv('.env')

bot_start = date.today().strftime("%d/%m/%Y")

welcome_room = int(os.getenv("WELROOM"))

class Ready(commands.Cog, name="Ready"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} พร้อมใช้งาน')
        print(bot_start)
        print("==================")
        await self.bot.get_channel(int(os.getenv("ADMINROOM"))).send(bot_start)
        await self.bot.change_presence(activity=nextcord.Game(name="Rov"))
    
def setup(bot:commands.Bot):
    bot.add_cog(Ready(bot))
    