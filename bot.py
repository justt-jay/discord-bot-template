import discord 
from discord import Embed
from discord.ext import commands
import requests
from discord_timestamps import format_timestamp, TimestampType
import json
import traceback


with open("config.json") as config_file:
    config = json.load(config_file)
prefix=config['prefix']
token=config['token']
  
bot = commands.Bot(command_prefix=prefix,help_command=None,description="A discord bot template using kiws bot api.")


@bot.command()
async def user(ctx,*,name):
 
  api = requests.get(f'https://api.kiwbot.org/user/{name}').json()
  if api['status'] == 404:
    em = discord.Embed(description='Please try again, this account is invalid, banned or doesn\'t exist',color=0xFF0000)
    await ctx.reply(embed=em)
  if api['status'] == 200:
      em = discord.Embed(title=f"@{api['data']['user']['uniqueId']}",description=api['data']['user']['signature'],url=f"https://tiktok.com/@{api['data']['user']['secUid']}",color=0x5865F2)
    
      em.add_field(name="Likes",value=api['data']['stats']['heartCount'])
      em.add_field(name="Followers",value=api['data']['stats']['followerCount'],inline=False)
      em.add_field(name="Following",value=api['data']['stats']['followingCount'])
      em.add_field(name="Videos",value=api['data']['stats']['videoCount'])
      em.add_field(name="Created at",value=format_timestamp(api['data']['user']['createTime'],TimestampType.SHORT_DATETIME))
      em.set_thumbnail(url=api['data']['user']['avatarThumb'])
      await ctx.send(embed=em)



@bot.command()
async def hashtag(ctx,*,hashtag):
 try: 
    api = requests.get(f'https://api.kiwbot.org/tag/{hashtag}')
    tag = api.json()['challenge']
    em = discord.Embed(title=f"{tag['title']}",discription=f"{tag['desc']}")
    em.add_field(name="")
 except KeyError as error:
   em = Embed(description="Please try again this hashtag does not exist, or something went wrong")
   await ctx.send(embed=em)



#----------------------------------------------------------------------------------------------------------------------------------------------------------


   
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(f"```py\n{error_msg}```")


@bot.event
async def on_ready():
  print("bots online")  
   

bot.run(token)    
