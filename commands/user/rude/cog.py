from nextcord.ext import commands
import random
import components as cp

class Rude(commands.Cog, name="Rude"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command(aliases=['ด่า'])
    async def rude(self, message,*, who=None):
        ranrude = random.choice(cp.rude)
        if who == None:
            await message.channel.send(ranrude)
        else:
            await message.channel.send(f"{who} {ranrude}")

def setup(bot:commands.Bot):
    bot.add_cog(Rude(bot))