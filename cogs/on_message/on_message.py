###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
from configs.config import config
from configs.config import get_lang
from configs.config import get_rank


timeflood=dict()
aviso = []

###########################################
# Class reformulada
###########################################

class on_message(commands.Cog):
    def __init__(self, client):
        self.client = client


###########################################
# Eventos On_message
###########################################
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        if message.content == self.client.user.mention:
         if get_rank(message.author.id, list(message.author.guild_permissions), message.guild.id, message.channel.id) >=1:
          lang = get_lang(message.guild.id, "on_message")
          if message.author.id in timeflood:
           w = json.loads(timeflood[message.author.id])
           if time.time() < w:
            if message.author.id in aviso:
               return
            aviso.append(message.author.id)
            embed = discord.Embed(description=str(lang['wait_little']).format(message.author.mention), color=0x7BCDE8)
            await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            aviso.remove(message.author.id)
          else:
            timeflood[message.author.id] = json.dumps(time.time()+10)
            lis = lang['prefix_warn']
            texto = random.choice(list(lis))
            embed = discord.Embed(description=str(texto).replace("{member_mention}",message.author.mention).replace("{prefix}",get_prefix(message.guild.id)), color=0x7BCDE8)
            await message.channel.send(embed=embed)


###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))
