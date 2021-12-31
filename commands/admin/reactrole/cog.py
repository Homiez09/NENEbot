import nextcord
import json

from nextcord.ext import commands

class Reactrole(commands.Cog, name="Reactrole"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.command() # reactrole
    @commands.has_guild_permissions(administrator=True)
    async def reactrole(sef, ctx, emoji, role: nextcord.Role,*,message):
        embed = nextcord.Embed(description = message, color=0x2ECC71)
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction(emoji)

        with open('reactrole.json') as f:
            data = json.load(f)

            new_react_role = {
                'role_name':role.name,
                'role_id':role.id,
                'emoji':emoji,
                'message_id': msg.id
            }

            data.append(new_react_role)

        with open('reactrole.json', 'w') as f:
            json.dump(data,f ,indent=4)     
            
def setup(bot:commands.Bot):
    bot.add_cog(Reactrole(bot))    