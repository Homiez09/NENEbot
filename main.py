# Made by Phumrapee Soenvanichakul (jannnn1235)
# Github: https://github.com/Jannnn1235/NENEbot


import random
import discord
import rudeList
import json
import requests
import table
import os

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

@bot.event
async def on_ready():
    print('{0.user}'.format(bot), 'is ready')
    print(bot_start)
    print("==================")
    await bot.change_presence(activity=discord.Game(name="n.help"))

@bot.event # USE FUNCTION
async def on_message(message):  
    await talk_with_bot(message) # TALK WITH BOT
    await pictureeiei(message)
    await show(message)
    #await talk_bot(message)
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
    if message.channel.id == 881090796319813642:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(f"imageRM/{attachment.filename}")
                await removebg(attachment.filename, message)
                print('Img has Saved.')

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
            channel = bot.get_channel(881090831119970314)
            await channel.send(file=file, content="ลบพื้นหลังเรียบร้อย (github : https://github.com/Jannnn1235/NENEbot)")         
    else:
        print("Error:", response.status_code, response.text)
        embederror = discord.Embed(description=f"เดือนนี้ใช้งานครบ 50 ครั้งแล้ว โปรดติดต่อ <@297740667784921089>", color=0x84c5e6)
        embederror.set_footer(text='github : https://github.com/Jannnn1235/NENEbot')
        await message.channel.send(embed=embederror)

@bot.event # TALK WITH BOT
async def talk_with_bot(message):
    if 'เนเน่ด่า' in message.content:   
        randomrude = random.choice(rudeList.rude)
        await message.channel.send(randomrude)

    if message.content.startswith('n.ด่า'):
        await message.delete()
    
    if message.content.startswith('n.nenesay'):
        await message.delete()

    if 'ตอนนี้กี่โมง' in message.content or 'ตอนนี้เวลา' in message.content:
        await message.channel.send(datetime.today().strftime("%H:%M"))

    if 'วันนี้วันที่' in message.content:
        await message.channel.send(datetime.today().strftime("%d/%m/%Y"))

@bot.event # SEND DM
async def sendDM(userid ,content=None):
    userid = int(userid)
    user = bot.get_user(userid)
    await user.send(content)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >= 3600:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} hours'.format(error.retry_after/3600), color=0xC70039)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        elif error.retry_after >= 360:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} minutes'.format(error.retry_after/60), color=0xC70039)
            await ctx.channel.send(embed=embeddelay, delete_after=5)
        else:
            embeddelay = discord.Embed(description='**You need to wait {:.0f} seconds'.format(error.retry_after), color=0xC70039)
            await ctx.channel.send(embed=embeddelay, delete_after=5)

@bot.event
async def show(message):
    search = message.content
    if message.channel.id == 881107013239734275 and message.author.id != 874845208704061492:
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=os.getenv("api_key")).cse()
        result = resource.list(
            q=f"{search}", cx="92f6c5f1da47c499a", searchType="image"        
        ).execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"นี่คือรูป{search}", color=0x84c5e6)
        embed1.set_image(url=url)
        await message.channel.send(embed=embed1)

@bot.event
async def talk_bot(message):    
    day_today = str(date.today().strftime("%A"))
    time_start = date.today().strftime("%H:%M")  
    if str(time_start) >= "08:10" and str(time_start) <= "08:30":
        x = 0
    elif str(time_start) >= "08:30" and str(time_start) <= "09:20":
        x = 1
    elif str(time_start) >= "09:20" and str(time_start) <= "10:10":
        x = 2
    elif str(time_start) >= "10:10" and str(time_start) <= "11:00":
        x = 3
    elif str(time_start) >= "11:00" and str(time_start) <= "11:50":
        x = 4
    elif str(time_start) >= "11:50" and str(time_start) <= "12:40":
        x = 5
    elif str(time_start) >= "12:40" and str(time_start) <= "13:30":
        x = 6
    elif str(time_start) >= "13:00" and str(time_start) <= "14:20":
        x = 7
    elif str(time_start) >= "14:20" and str(time_start) <= "15:10":
        x = 8
    elif str(time_start) >= "15:10" and str(time_start) <= "16:00":
        x = 9
    else:
        x = 10

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
        embed=discord.Embed(title="ช่วยเหลือ" , color=0x84c5e6)
        embed.add_field(name="คาบนี้", value="พิมพ์ในช่องแชท", inline=False)
        embed.add_field(name="คาบต่อไป", value="พิมพ์ในช่องแชท", inline=False)
        embed.add_field(name="ตารางเรียน", value="พิมพ์ในช่องแชท", inline=True)
        embed.set_thumbnail(url = bot.user.avatar_url)
        embed.set_footer(text="github : https://github.com/Jannnn1235/NENEbot")
        await message.channel.send(embed=embed)

@bot.command() # clear
@commands.has_guild_permissions(administrator=True)
@commands.cooldown(1,3,commands.BucketType.user)
async def clear(ctx, limit=5):
    await ctx.channel.purge(limit=limit+1)

@bot.command() # info
@commands.cooldown(1,5,commands.BucketType.user)
async def info(message):
    embed=discord.Embed(title="บัตรประจำตัวประชาชน" , color=0x84c5e6)
    embed.add_field(name="ชื่อผู้ใช้", value=f"{message.author.name}", inline=False)
    embed.add_field(name="เลขบัตรประจำตัว", value=f"{message.author.id}", inline=False)
    embed.add_field(name="ที่อยู่ปัจจุบัน", value=f"{message.author.guild}", inline=True)
    embed.set_thumbnail(url = message.author.avatar_url)
    embed.set_footer(text="github : https://github.com/Jannnn1235/NENEbot")
    await message.send(embed=embed)
    
@bot.command() # ด่า
@commands.cooldown(1,5,commands.BucketType.user)
async def ด่า(message,*, who):
    eiei = who
    ranrude = random.choice(rudeList.rude)
    await message.channel.send(f"{eiei} {ranrude}")

@bot.command() # send_dm
@commands.has_role(int(os.getenv("role")))
@commands.cooldown(1,3,commands.BucketType.user)
async def send_dm(ctx, member:discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

@bot.command() # reactrole
@commands.has_guild_permissions(administrator=True)
async def reactrole(ctx, emoji, role: discord.Role,*,message):
    embed = discord.Embed(description = message, color=0x2ECC71)
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

@bot.command() # online
async def online(ctx):
    global bot_start
    embedonline = discord.Embed(description=f"Nene กำลังทำงาน", color=0x84c5e6)
    embedonline.set_footer(text='github : https://github.com/Jannnn1235/NENEbot')
    await ctx.channel.send(embed=embedonline)

@bot.command() # nenesay
@commands.has_guild_permissions(administrator=True)
async def nenesay(ctx,* ,message):
    embed = discord.Embed(description = message, color=0x2ECC71)
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

''' @bot.command()
@commands.has_guild_permissions(administrator=True)
async def kickass(ctx):
    file = discord.File("image/Thanos.gif")
    await ctx.channel.send(file = file)
    for members in ctx.author.voice.channel.members:    
        await members.move_to(None)
        await ctx.send(f'{members} was killed by Thanos.') '''

bot.run(os.getenv("TOKEN"))

skyblue = 0x84c5e6
yellow = 0xD4AC0D
green = 0x2ECC71
red = 0xC70039


