# Made by Phumrapee Soenvanichakul (HomieZ09)
# Github: https://github.com/Homiez09/NENEbot
import random
import nextcord
import json
import requests
import os

import components as cp

from ntpath import join
from re import purge
from nextcord.ext import commands
from datetime import datetime
from nextcord.ext.commands.core import command
from googleapiclient.discovery import build
from nextcord.ext.commands import check
from nextcord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime as date
from dotenv import load_dotenv
from nextcord.utils import get 

load_dotenv('.env')

bot_start = datetime.today().strftime("%d/%m/%Y")

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents = nextcord.Intents().all())

welcome_room = int(os.getenv("WELROOM"))

github = "github : https://github.com/Homiez09/NENEbot"\

blue = 0x84c5e6
yellow = 0xD4AC0D
green = 0x2ECC71
red = 0xC70039

def randomQuote(mode):
    if mode == "love":
        quote_love = cp.quoteList["love"]
        ranq = random.choice(quote_love)
        return ranq
    elif mode == "sad":
        quote_sad = cp.quoteList["sad"]
        ranq = random.choice(quote_sad)       
        return ranq
    else: 
        return "```>> n.quote [love/sad]``` "
    
@bot.event
async def on_ready():
    print(f'{bot.user} พร้อมใช้งาน')
    print(bot_start)
    print("==================")
    await bot.get_channel(int(os.getenv("ADMINROOM"))).send(bot_start)
    await bot.change_presence(activity=nextcord.Game(name=f"{os.getenv('PREFIX')}help"))

@bot.event
async def on_member_join(member):
    embed=nextcord.Embed(description=f"{member.name} has joined." , color=green)
    await bot.get_channel(welcome_room).send(embed = embed)

@bot.event
async def on_member_remove(member):
    embed=nextcord.Embed(description=f"{member.name} has leaved." , color=red)
    await bot.get_channel(welcome_room).send(embed = embed)

@bot.event # USE FUNCTION
async def on_message(message):  
    await talk_with_bot(message)
    await pictureeiei(message)
    await send_pic_in_room(message)
    await talk_bot(message)
    await bot.process_commands(message) 

@bot.event 
async def on_raw_reaction_add(payload):
    if payload.member.bot:
        pass   
    else:
        with open('reactrole.json') as f:
            data = json.load(f)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = nextcord.utils.get(bot.get_guild(payload.guild_id).roles, id=x["role_id"])
                    await payload.member.add_roles(role)

image_types = ["png", "jpeg", "jpg"]
@bot.event # USE FUNCTION
async def pictureeiei(message):
    if message.channel.id == int(os.getenv("INPUTCH")):
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(f"imageRM/{attachment.filename}")
                await removebg(attachment.filename, message)

@bot.event
async def removebg(filenames, message):
    filenames = filenames
    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(f'imageRM/{filenames}', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': os.getenv("REBG")},
    )
    if response.status_code == requests.codes.ok:
        with open('imageRM/remove/NENE_BOT.png', 'wb') as out:
            out.write(response.content)
            file = nextcord.File("imageRM/remove/NENE_BOT.png")
            channel = bot.get_channel(int(os.getenv("OUTPUTCH")))
            await channel.send(file=file, content=f"ลบพื้นหลังเรียบร้อย")         
    else:
        embederror = nextcord.Embed(description=f"เดือนนี้ใช้งานเกินขีดจำกัดแล้ว Contact: <@297740667784921089>", color=red)
        await message.channel.send(embed=embederror)

@bot.event # TALK WITH BOT
async def talk_with_bot(message):
    if 'เนเน่ด่า' in message.content:   
        randomrude = random.choice(cp.rude)
        await message.channel.send(randomrude)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >= 3600:
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} hours'.format(error.retry_after/3600), color=red)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        elif error.retry_after >= 360:
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} minutes'.format(error.retry_after/60), color=red)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        else:
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} seconds'.format(error.retry_after), color=red)
            await ctx.channel.send(embed=embeddelay, delete_after=5)

@bot.event
async def send_pic_in_room(message):
    search = message.content
    if message.channel.id == int(os.getenv("SEARCHCH")) and message.author.id != bot.user.id:
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=os.getenv("api_key")).cse()
        result = resource.list(
            q=f"{search}", cx="92f6c5f1da47c499a", searchType="image"        
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = nextcord.Embed(title=f"นี่คือรูป{search}", color=blue)
        embed1.set_image(url=url)
        await message.channel.send(embed=embed1)

@bot.event
async def talk_bot(message):    
    def findX():
        for i in range(len(time)): # len 11 i_max = 10
            if i == 10:
                return i
            elif time_start > time[i] and time_start < time[i+1]:
                return i

    day_today = str(date.today().strftime("%A"))
    time_start = date.today().strftime("%H:%M")  
    time_start = str(time_start)
    time = cp.table["timestart"] 
    day = cp.table["day"]
    x = findX()
                
    if "คาบนี้" in message.content:
        if day_today in day and x < 10:
            await message.channel.send(f"{day[f'{day_today}'][x]} {time[x]} - {time[x+1]}")
        else:
                await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก") 
                    
    if "คาบต่อไป" in message.content or "คาบหน้า" in message.content:
        if day_today in day and x < 9:
            await message.channel.send(day[f"{day_today}"][x+1])
        else:
            await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")    
            
    if "คาบที่แล้ว" in message.content or "คาบเมื่อกี้" in message.content:
        if day_today in day and x > 0 and x < 10:
            await message.channel.send(day[f"{day_today}"][x-1])
        else:
            await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")   

    if 'ตารางเรียน' in message.content:   
        file = nextcord.File("image/ตารางเรียน.jpg")
        await message.channel.send(file = file)

@bot.command() # clear
@commands.has_guild_permissions(administrator=True)
@commands.cooldown(1,3,commands.BucketType.user)
async def clear(ctx, limit=5):
    await ctx.channel.purge(limit=limit+1)

@bot.command() # info
@commands.cooldown(1,5,commands.BucketType.user)
async def myinfo(message):
    embed=nextcord.Embed(title="บัตรประจำตัวประชาชน" , color=blue)
    embed.add_field(name="ชื่อผู้ใช้", value=f"{message.author.name}", inline=False)
    embed.add_field(name="เลขบัตรประจำตัว", value=f"{message.author.id}", inline=False)
    embed.add_field(name="ที่อยู่ปัจจุบัน", value=f"{message.author.guild}", inline=True)
    embed.set_thumbnail(url = message.author.display_avatar.url)
    await message.send(embed=embed)
    
@bot.command(aliases=['ด่า']) # rude
@commands.cooldown(1,5,commands.BucketType.user)
async def rude(message,*, who):
    who = who
    ranrude = random.choice(cp.rude)
    await message.channel.send(f"{who} {ranrude}")

@bot.command() # reactrole
@commands.has_guild_permissions(administrator=True)
async def reactrole(ctx, emoji, role: nextcord.Role,*,message):
    embed = nextcord.Embed(description = message, color=green)
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

@bot.command() # nenesay
@commands.has_guild_permissions(administrator=True)
async def nenesay(ctx,* ,message):
    embed = nextcord.Embed(description = message, color=green)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def move(ctx, channel : nextcord.VoiceChannel):
    try:    
        for members in ctx.author.voice.channel.members:
            embed = nextcord.Embed(description=f'Move {members} to {channel}', color=green)
            await members.move_to(channel)
            await ctx.send(embed = embed)
    except:
        embed = nextcord.Embed(description='Something Went Wrong!!', color=green)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def snap(ctx):
    try:    
        for members in ctx.author.voice.channel.members:
            await members.move_to(None)
            await ctx.send("https://cdn.discordapp.com/attachments/875313424601612318/925727431644561499/Thanos.gif")
            await ctx.send(f"{members.mention} was slain by Thanos, for the good of the Universe.")
    except:
        embed = nextcord.Embed(description='Something Went Wrong!!', color=green)
        await ctx.send(embed=embed)
        

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def show(ctx, search):   # show picture        
    search = search
    print(search)
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=os.getenv("api_key")).cse()
    result = resource.list(
        q=f"{search}", cx="92f6c5f1da47c499a", searchType="image"        
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = nextcord.Embed(title=f"นี่คือรูป{search}", color=blue)

    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

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

@bot.command(aliases=['q'])
@commands.cooldown(1,3,commands.BucketType.user)
async def quote(ctx): # quote
    view = QuoteButton()
    embed = nextcord.Embed(description="กดปุ่มเพื่อเลือก | Which one?", color=blue)
    await ctx.send(embed=embed, view=view)
    await view.wait()

bot.run(os.getenv("TOKEN"))