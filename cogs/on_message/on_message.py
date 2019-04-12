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



timeflood=dict()
aviso = []
aviso_2 = []
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
        if message.content == f"<@!{self.client.user.id}>":
         if get_rank(message.author.id, list(message.author.guild_permissions), message.guild.id, message.channel.id) >=1:
          lang = get_lang(message.guild.id, "on_message")
          if message.author.id in aviso_2:
             return

          if message.author.id in aviso:
             embed = discord.Embed(description=str(lang['wait_little']).format(message.author.mention), color=0x7BCDE8)
             await message.channel.send(embed=embed)
             aviso_2.append(message.author.id)
             await asyncio.sleep(7)
             aviso_2.remove(message.author.id)
          else:
            lis = lang['prefix_warn']
            texto = random.choice(list(lis))
            embed = discord.Embed(description=str(texto).replace("{member_mention}",message.author.mention).replace("{prefix}",get_prefix(message.guild.id)), color=0x7BCDE8)
            await message.channel.send(embed=embed)
            aviso.append(message.author.id)
            await asyncio.sleep(4)
            aviso.remove(message.author.id)

        if message.content == self.client.user.mention:
         if get_rank(message.author.id, list(message.author.guild_permissions), message.guild.id, message.channel.id) >=1:
          lang = get_lang(message.guild.id, "on_message")
          if message.author.id in aviso_2:
             return

          if message.author.id in aviso:
             embed = discord.Embed(description=str(lang['wait_little']).format(message.author.mention), color=0x7BCDE8)
             await message.channel.send(embed=embed)
             aviso_2.append(message.author.id)
             await asyncio.sleep(7)
             aviso_2.remove(message.author.id)
          else:
            lis = lang['prefix_warn']
            texto = random.choice(list(lis))
            embed = discord.Embed(description=str(texto).replace("{member_mention}",message.author.mention).replace("{prefix}",get_prefix(message.guild.id)), color=0x7BCDE8)
            await message.channel.send(embed=embed)
            aviso.append(message.author.id)
            await asyncio.sleep(4)
            aviso.remove(message.author.id)
###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))
