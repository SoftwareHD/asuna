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
import pytz
from datetime import datetime
from configs.config import *


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

timeflood=dict()
aviso = []

###########################################
# Class reformulada
###########################################

class status_asuna(commands.Cog):
    def __init__(self, client):
        self.client = client


###########################################
# Eventos status_asuna
###########################################
    @commands.Cog.listener()
    async def on_ready(self):
      while True:
       server = self.client.get_guild(int(config["guild_asuna"]))
       channel = discord.utils.get(server.channels, id=int(config["status"]))
       user = discord.utils.get(server.members, id=int(config["yuka"]))
       message = await channel.fetch_message(int(config["id_status"]))
       time = str(datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H:%M:%S - %d/%m/20%y")) 
       try:
          lang = get_lang(server.id, "botinfo")
          mem = get_memory()
          embed = discord.Embed(colour=0x7BCDE8)
          embed.set_author(name=str(lang["title_embed_2"]).format(self.client.user.name), icon_url=user.avatar_url_as())
          embed.add_field(name=str(lang["created_by"]), value = '``Yuka Tuka#8484``', inline=True)
          embed.add_field(name=str(lang["tag"]), value = '``'+str(self.client.user)+'``', inline=True)
          embed.add_field(name=str(lang["ids"]), value = '``'+str(self.client.user.id)+'``', inline=True)
          embed.add_field(name=str(lang["api"]), value = '``Discord.py '+str(discord.__version__)+'``', inline=True)
          embed.add_field(name=str(lang["python"]), value = '``'+str(sys.version[:5])+'``', inline=True)
          embed.add_field(name=str(lang["memory"]), value = '``'+str(mem["memory_used"])+'/'+str(mem["memory_total"])+' ('+str(mem["memory_percent"])+')``', inline=True)
          embed.add_field(name=str(lang["uptime"]), value = '``'+str(timetotal()).replace("{day}",lang["day"]).replace("{hour}",lang["hour"]).replace("{minute}",lang["minute"]).replace("{second}",lang["second"])+'``', inline=True)
          embed.add_field(name=str(lang["servers"]), value = '``'+str(len(self.client.guilds))+' (shards '+str(config["shard_count"])+')``', inline=True)
          embed.add_field(name=str(lang["ping"]), value = '``{0:.2f}ms``'.format(self.client.latency * 1000), inline=True)
          embed.add_field(name=str(lang["prefix"]), value = '``'+str(get_prefix(server.id))+'``', inline=True)
          embed.add_field(name=str(lang["update"]), value = '``'+str(time)+'``', inline=True)

          embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
          await message.edit(embed=embed)
          await asyncio.sleep(3600)
       except Exception as e:
           await message.edit(e)
 

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(status_asuna(client))
