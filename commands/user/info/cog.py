import nextcord
from nextcord.ext import commands

class Info(commands.Cog, name="Info"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def info(self, message):
        embed=nextcord.Embed(title="บัตรประจำตัวประชาชน" , color=0x84c5e6)
        embed.add_field(name="ชื่อผู้ใช้", value=f"{message.author.name}", inline=False)
        embed.add_field(name="เลขบัตรประจำตัว", value=f"{message.author.id}", inline=False)
        embed.add_field(name="ที่อยู่ปัจจุบัน", value=f"{message.author.guild}", inline=True)
        embed.set_thumbnail(url = message.author.display_avatar.url)
        await message.send(embed=embed)
        
def setup(bot:commands.Bot):
    bot.add_cog(Info(bot))