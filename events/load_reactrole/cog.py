import nextcord
import json

from nextcord.ext import commands

class ReactroleEvent(commands.Cog, name="reactroleEvent"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            pass   
        else:
            with open('reactrole.json') as f:
                data = json.load(f)
                for x in data:
                    if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                        role = nextcord.utils.get(self.bot.get_guild(payload.guild_id).roles, id=x["role_id"])
                        await payload.member.add_roles(role)
    
def setup(bot:commands.Bot):
    bot.add_cog(ReactroleEvent(bot))
    