# Made by Phumrapee Soenvanichakul (Homiez09)
# Github: https://github.com/Homiez09/NENEbot
import random
import nextcord
import json
import requests
import os

import components as cp

from nextcord.ext import commands
from datetime import datetime
from googleapiclient.discovery import build
from datetime import datetime as date
from dotenv import load_dotenv

load_dotenv('.env')

bot_start = datetime.today().strftime("%d/%m/%Y")

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents = nextcord.Intents().all())

welcome_room = int(os.getenv("WELROOM"))
ADMINROOM = int(os.getenv("ADMINROOM"))

github = "github : https://github.com/Homiez09/NENEbot"\

async def on_ready():
    print('{0.user}'.format(bot), 'is ready')
    print(bot_start)
    print("==================")
    await bot.change_presence(activity=nextcord.Game(name="Binance"))

for folder in os.listdir("events"):
    if os.path.exists(os.path.join("events", folder, "cog.py")):
        bot.load_extension(f"events.{folder}.cog")

for folder in os.listdir("commands/user"):
    if os.path.exists(os.path.join("commands/user", folder, "cog.py")):
        bot.load_extension(f"commands.user.{folder}.cog")

for folder in os.listdir("commands/admin"):
    if os.path.exists(os.path.join("commands/admin", folder, "cog.py")):
        bot.load_extension(f"commands.admin.{folder}.cog")

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
        embederror = nextcord.Embed(description=f"เดือนนี้ใช้งานเกินขีดจำกัดแล้ว Contact: <@297740667784921089>", color=cp.color["red"])
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
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} hours'.format(error.retry_after/3600), color=cp.color["red"])
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        elif error.retry_after >= 360:
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} minutes'.format(error.retry_after/60), color=cp.color["red"])
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        else:
            embeddelay = nextcord.Embed(description='**You need to wait {:.0f} seconds'.format(error.retry_after), color=cp.color["red"])
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
        embed1 = nextcord.Embed(title=f"นี่คือรูป{search}", color=cp.color["blue"])
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
                
    if "คาบนี้" in message.content:
        x = findX()
        if day_today in day and x < 10:
            await message.channel.send(f"{day[f'{day_today}'][x]} {time[x]} - {time[x+1]}")
        else:
                await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก") 
                    
    if "คาบต่อไป" in message.content or "คาบหน้า" in message.content:
        x = findX()
        if day_today in day and x < 9:
            await message.channel.send(day[f"{day_today}"][x+1])
        else:
            await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")    
            
    if "คาบที่แล้ว" in message.content or "คาบเมื่อกี้" in message.content:
        x = findX()
        if day_today in day and x > 0 and x < 10:
            await message.channel.send(day[f"{day_today}"][x-1])
        else:
            await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")   

    if 'ตารางเรียน' in message.content:   
        file = nextcord.File("image/ตารางเรียน.jpg")
        await message.channel.send(file = file)

bot.run(os.getenv("TOKEN"))