# Made by Phumrapee Soenvanichakul (jannnn1235)
# Github: https://github.com/Jannnn1235/NENEbot
import random
import discord
import json
import requests
import os

import table
import rudeList
import quoteList

from ntpath import join
from re import purge
from discord.ext import commands
from datetime import datetime
from discord.ext.commands.core import command
from googleapiclient.discovery import build
from discord.ext.commands import check
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime as date
from dotenv import load_dotenv
from discord.utils import get 

load_dotenv('.env')

bot_start = datetime.today().strftime("%d/%m/%Y")

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents = discord.Intents().all())

welcome_room = int(os.getenv("WELROOM"))

github = "github : https://github.com/Jannnn1235/NENEbot"\

blue = 0x84c5e6
yellow = 0xD4AC0D
green = 0x2ECC71
red = 0xC70039

def randomQuote(mode):
    if mode == "love":
        quote_love = quoteList.love
        ranq = random.choice(quote_love)
        return ranq
    elif mode == "sad":
        quote_sad = quoteList.sad
        ranq = random.choice(quote_sad)       
        return ranq
    else: 
        return "You have to type ```n.quote [love/sad]``` "
    
@bot.event
async def on_ready():
    print(f'{bot.user} พร้อมใช้งาน')
    print(bot_start)
    print("==================")
    await bot.change_presence(activity=discord.Game(name="n.help"))

@bot.event
async def on_member_join(member):
    embed=discord.Embed(description=f"{member.name} has joined." , color=green)
    await bot.get_channel(welcome_room).send(embed = embed)

@bot.event
async def on_member_remove(member):
    embed=discord.Embed(description=f"{member.name} has leaved." , color=red)
    await bot.get_channel(welcome_room).send(embed = embed)

@bot.event # USE FUNCTION
async def on_message(message):  
    await talk_with_bot(message) # TALK WITH BOT
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
                    role = discord.utils.get(bot.get_guild(payload.guild_id).roles, id=x["role_id"])
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
            file = discord.File("imageRM/remove/NENE_BOT.png")
            channel = bot.get_channel(int(os.getenv("OUTPUTCH")))
            await channel.send(file=file, content=f"ลบพื้นหลังเรียบร้อย")         
    else:
        #print("Error:", response.status_code, response.text)
        embederror = discord.Embed(description=f"เดือนนี้ใช้งานเกินขีดจำกัดแล้ว Contact: <@297740667784921089>", color=red)
        await message.channel.send(embed=embederror)

@bot.event # TALK WITH BOT
async def talk_with_bot(message):
    if 'เนเน่ด่า' in message.content:   
        randomrude = random.choice(rudeList.rude)
        await message.channel.send(randomrude)

    if 'ตอนนี้กี่โมง' in message.content or 'ตอนนี้เวลา' in message.content:
        await message.channel.send(datetime.today().strftime("%H:%M"))

    if 'วันนี้วันที่' in message.content:
        await message.channel.send(datetime.today().strftime("%d/%m/%Y"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >= 3600:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} hours'.format(error.retry_after/3600), color=red)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        elif error.retry_after >= 360:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} minutes'.format(error.retry_after/60), color=red)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        else:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} seconds'.format(error.retry_after), color=red)
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
        embed1 = discord.Embed(title=f"นี่คือรูป{search}", color=blue)
        embed1.set_image(url=url)
        await message.channel.send(embed=embed1)

@bot.event
async def talk_bot(message):    
    day_today = str(date.today().strftime("%A"))
    time_start = date.today().strftime("%H:%M")  

    def findX():
        for i in range(11):
            if str(time_start) >= table.timestart['timestart'][i] and str(time_start) <= table.timestart['timestart'][i+1]:
                return i
            elif i == 10:
                return i

    if 'คาบ' in message.content:
        x = findX()
        if 'คาบนี้' in message.content:  
            if day_today in table.day and x < 10:
                await message.channel.send(f"{table.day[f'{day_today}'][x]} {table.timestart['timestart'][x]} - {table.timestart['timestart'][x+1]}")
            else:
                await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")

        if 'คาบต่อไป' in message.content or 'คาบหน้า' in message.content:
            if day_today in table.day and x < 9:
                await message.channel.send(table.day[f"{day_today}"][x+1])
            else:
                await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")
        
        if 'คาบเมื่อกี้' in message.content or 'คาบที่แล้ว' in message.content:  
            if day_today in table.day and x < 10:
                await message.channel.send(table.day[f"{day_today}"][x-1])
            else:
                await message.channel.send("ไม่มีเรียนไอ้สัสเอ้ย อย่าติดตลก")

    if 'ตารางเรียน' in message.content:   
        file = discord.File("image/ตารางเรียน.jpg")
        await message.channel.send(file = file)

    if message.content == 'n.help':
        embed=discord.Embed(title="ช่วยเหลือ" , color=blue)
        embed.add_field(name="คาบนี้", value="พิมพ์ในช่องแชท", inline=False)
        embed.add_field(name="คาบต่อไป", value="พิมพ์ในช่องแชท", inline=False)
        embed.add_field(name="ตารางเรียน", value="พิมพ์ในช่องแชท", inline=True)
        embed.set_thumbnail(url = bot.user.avatar_url)
        await message.channel.send(embed=embed)

@bot.command() # clear
@commands.has_guild_permissions(administrator=True)
@commands.cooldown(1,3,commands.BucketType.user)
async def clear(ctx, limit=5):
    await ctx.channel.purge(limit=limit+1)

@bot.command() # info
@commands.cooldown(1,5,commands.BucketType.user)
async def myinfo(message):
    embed=discord.Embed(title="บัตรประจำตัวประชาชน" , color=blue)
    embed.add_field(name="ชื่อผู้ใช้", value=f"{message.author.name}", inline=False)
    embed.add_field(name="เลขบัตรประจำตัว", value=f"{message.author.id}", inline=False)
    embed.add_field(name="ที่อยู่ปัจจุบัน", value=f"{message.author.guild}", inline=True)
    embed.set_thumbnail(url = message.author.avatar_url)
    await message.send(embed=embed)
    
@bot.command(aliases=['ด่า']) # rude
@commands.cooldown(1,5,commands.BucketType.user)
async def rude(message,*, who):
    who = who
    ranrude = random.choice(rudeList.rude)
    await message.channel.send(f"{who} {ranrude}")

@bot.command(aliases=['dm']) # send_dm
@commands.has_role(int(os.getenv("role")))
@commands.cooldown(1,3,commands.BucketType.user)
async def send_dm(ctx, member:discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

@bot.command() # reactrole
@commands.has_guild_permissions(administrator=True)
async def reactrole(ctx, emoji, role: discord.Role,*,message):
    embed = discord.Embed(description = message, color=green)
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

@bot.command(aliases=['github', 'info']) # online
async def online(ctx):
    global bot_start
    embedonline = discord.Embed(description=f"Nene กำลังทำงาน", color=blue)
    embedonline.set_footer(text='github : https://github.com/Jannnn1235/NENEbot')
    await ctx.channel.send(embed=embedonline)

@bot.command() # nenesay
@commands.has_guild_permissions(administrator=True)
async def nenesay(ctx,* ,message):
    embed = discord.Embed(description = message, color=green)
    await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def move(ctx, channel : discord.VoiceChannel):
    try:
        await ctx.member.disconnect()
    except:
        for members in ctx.author.voice.channel.members:
            await members.move_to(None)
            await ctx.send(f'move {members} to {channel}')

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
    embed1 = discord.Embed(title=f"นี่คือรูป{search}", color=blue)

    embed1.set_image(url=url)
    await ctx.send(embed=embed1)

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def quote(ctx, mode=None):
    await ctx.send(randomQuote(mode))

bot.run(os.getenv("TOKEN"))