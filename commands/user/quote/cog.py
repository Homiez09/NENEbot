import random
import nextcord
import components as cp 

from nextcord.ext import commands

def randomQuote(mode):
    return random.choice(cp.quoteList[f'{mode}'])
        
class QuoteButton(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            
        @nextcord.ui.button(label="Love 💖", style=nextcord.ButtonStyle.success)
        async def love(self, button, interaction):
            await interaction.response.send_message(randomQuote("love"))
            self.value = "love"
            self.stop()
        @nextcord.ui.button(label="Sad 😭", style=nextcord.ButtonStyle.success)
        async def sad(self, button, interaction):
            await interaction.response.send_message(randomQuote("sad")) 
            self.value = "sad"
            self.stop()
            
class Quote(commands.Cog, name="quote"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.command(aliases=['q'])
    async def quote(self, ctx): # quote
        view = QuoteButton()
        embed = nextcord.Embed(description="กดปุ่มเพื่อเลือก | Which one?", color=0x84c5e6)
        await ctx.send(embed=embed, view=view)
        await view.wait()
    
def setup(bot:commands.Bot):
    bot.add_cog(Quote(bot))