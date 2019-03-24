###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
import sys
import psutil
import os
from configs.config import config
from configs.config import get_lang
from configs.config import get_rank

startTime = time.time()
def getUptime():
  return time.time() - startTime

def timetotal():
  total_seconds = float(getUptime())
  MINUTE = 60
  HOUR = MINUTE * 60
  DAY = HOUR * 24
  days = int( total_seconds / DAY )
  hours = int( ( total_seconds % DAY ) / HOUR )
  minutes = int( ( total_seconds % HOUR ) / MINUTE )
  seconds = int( total_seconds % MINUTE )
  string = ""
  if days > 0:
    string += str(days) + " " + (days == 1 and "{day}" or "{day}s" ) + ", "
  if len(string) > 0 or hours > 0:
    string += str(hours) + " " + (hours == 1 and "{hour}" or "{hour}s" ) + ", "
  if len(string) > 0 or minutes > 0:
    string += str(minutes) + " " + (minutes == 1 and "{minute}" or "{minute}s" ) + ", "
  string += str(seconds) + " " + (seconds == 1 and "{second}" or "{second}s" )
  return string;

def get_memory():
    memory = dict()
    mem = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    process = process.memory_info().rss 
    swap = psutil.swap_memory()
    memory['memory_used'] = f'{mem.used / 0x40_000_000:.2f}'
    memory['memory_available'] = f'{mem.available / 0x40_000_000:.2f}'
    memory['memory_total'] = f'{mem.total / 0x40_000_000:.2f}'
    memory['memory_free'] = f'{mem.free / 0x40_000_000:.2f}'
    memory['memory_percent'] = str(mem.percent)+'%'
    memory['process_python'] = f'{process / 1024/1024:.2f}'
    return memory


###########################################
# Class reformulada
###########################################

class botinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def botinfo(self,ctx):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
          lang = get_lang(ctx.guild.id, "botinfo")
          mem = get_memory()
          embed = discord.Embed(description=str(lang['description_embed']).format(ctx.author.name, self.client.user.name),colour=0x7BCDE8)
          embed.set_author(name=str(lang["title_embed"]).format(self.client.user.name), icon_url=ctx.author.avatar_url_as())
          embed.add_field(name=str(lang["created_by"]), value = '``Yuka Tuka#8484``', inline=True)
          embed.add_field(name=str(lang["tag"]), value = '``'+str(self.client.user)+'``', inline=True)
          embed.add_field(name=str(lang["ids"]), value = '``'+str(self.client.user.id)+'``', inline=True)
          embed.add_field(name=str(lang["api"]), value = '``Discord.py '+str(discord.__version__)+'``', inline=True)
          embed.add_field(name=str(lang["python"]), value = '``'+str(sys.version[:5])+'``', inline=True)
          embed.add_field(name=str(lang["memory"]), value = '``'+str(mem["memory_used"])+'/'+str(mem["memory_total"])+' ('+str(mem["memory_percent"])+')``', inline=True)
          embed.add_field(name=str(lang["uptime"]), value = '``'+str(timetotal()).replace("{day}",lang["day"]).replace("{hour}",lang["hour"]).replace("{minute}",lang["minute"]).replace("{second}",lang["second"])+'``', inline=True)
          embed.add_field(name=str(lang["servers"]), value = '``'+str(len(self.client.guilds))+' (shards '+str(config["shard_count"])+')``', inline=True)
          embed.add_field(name=str(lang["ping"]), value = '``{0:.2f}ms``'.format(self.client.latency * 1000), inline=True)
          embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
          await ctx.send(embed=embed)
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(botinfo(client))
