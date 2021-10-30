# Made by Phumrapee Soenvanichakul (jannnn1235)
# Github: https://github.com/Jannnn1235/NENEbot

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv('.env')
#bot = commands.Bot(command_prefix=config.PREFIX["command"], intents=discord.Intents().all())
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents = discord.Intents().all())

@bot.event
async def on_ready():
    print('{0.user}'.format(bot), 'is ready')
    print("==================")
    await bot.change_presence(activity=discord.Game(name="Thanos Glove"))

@bot.event
async def on_message(message):  
    await bot.process_commands(message) 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("**Invalid command.**")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Please pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**You don't have permission**")

@bot.command(aliases=['getout', 'fuck', 'ดีด'])
@commands.has_guild_permissions(administrator=True)
async def snap(ctx):
    try:
        if ctx.author.voice.channel.members != "":
            print('Working...')
            file = discord.File("image/Thanos.gif")
            await ctx.channel.send(file = file)
            for members in ctx.author.voice.channel.members:    
                await members.move_to(None)
                #embed = discord.Embed(description=f'{members.mention} was slain by Thanos, for the good of the Universe.')
                await ctx.send(f'{members.mention} was slain by Thanos, for the good of the Universe.')
    except:
        await ctx.send('No one in voice channel.')

bot.run(os.getenv("TOKEN"))