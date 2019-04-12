###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
import requests
import sys
import psutil
import os
import pytz
import textwrap
from io import BytesIO
from datetime import datetime
from configs.config import *

def haste(text):
    try:
      response = requests.post("https://hastebin.com/documents", data={'text':text}, headers={"User-Agent":"Mozilla/5.0"})
      return "https://hastebin.com/"+str(json.loads(response.text)['key'])
    except Exception as e:
        return e



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
    async def on_message_edit(self, before, after):
       if before.author.bot == False:
        if before.content != after.content:
          guild_db = date_server_cache(before.guild.id)
          if guild_db["modlog"]["status"] == False:
              return
          if guild_db["modlog"]["channel"] == None:
              return                
          if guild_db["modlog"]["message_edit"] == "on":
          
           lang = get_lang(before.guild.id, "modlog")  
           embed=discord.Embed(color=0x7BCDE8)
           embed.set_author(name=str(lang["edited"]), icon_url=before.author.avatar_url)
           if len(before.attachments) >=1:
             link = before.attachments[0].url
             url = str(link).replace("https://cdn.discordapp.com/","https://media.discordapp.net/")
             embed.set_image(url=url)
           else:
             pass
           if len(before.content) >=1:
             embed.add_field(name=str(lang["edited_1"]), value=f"``{before.content[:900]}``", inline=True)
             embed.add_field(name=str(lang["edited_2"]), value=f"``{after.content[:900]}``", inline=True)
           else:
             pass          
           embed.add_field(name=str(lang["user"]), value=f"``{before.author}`` - (<@{before.author.id}>)", inline=True)
           embed.add_field(name=str(lang["channel"]), value=f"``{before.channel.name}`` - (<#{before.channel.id}>)", inline=True)
           timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
           time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))          
           embed.add_field(name=str(lang["time"]), value=f"``{time}``", inline=True)
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           canal = discord.utils.get(before.guild.channels, id=int(guild_db["modlog"]["channel"]))
           if canal is None:
              return
           await canal.send(embed=embed)
 
    @commands.Cog.listener()
    async def on_message_delete(self, message):
       if message.author.bot == False:
          guild_db = date_server_cache(message.guild.id)
          if guild_db["modlog"]["status"] == False:
              return
          if guild_db["modlog"]["channel"] == None:
              return
          if guild_db["modlog"]["message_delete"] == "on":
           lang = get_lang(message.guild.id, "modlog")
           embed=discord.Embed(color=0x7BCDE8)
           embed.set_author(name=str(lang["delet"]), icon_url=message.author.avatar_url)
           if len(message.attachments) >=1:
             link = message.attachments[0].url
             url = str(link).replace("https://cdn.discordapp.com/","https://media.discordapp.net/")
             embed.set_image(url=url)
           else:
             pass
           if len(message.content) >=1:
              embed.add_field(name=str(lang["delet_1"]), value=f"``{message.content[:900]}``", inline=True)
           else:
             pass          
           embed.add_field(name=str(lang["user"]), value=f"``{message.author}`` - (<@{message.author.id}>)", inline=True)
           embed.add_field(name=str(lang["channel"]), value=f"``{message.channel.name}`` - (<#{message.channel.id}>)", inline=True)
           timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
           time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))          
           embed.add_field(name=str(lang["time"]), value=f"``{time}``", inline=True)
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           canal = discord.utils.get(message.guild.channels, id=int(guild_db["modlog"]["channel"]))
           if canal is None:
             return
           await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        logs = []
        if messages:
          channel = messages[0].channel
          guild = channel.guild
          guild_db = date_server_cache(guild.id)

          if guild_db["modlog"]["status"] == False:
              return
          if guild_db["modlog"]["channel"] == None:
              return
          if guild_db["modlog"]["message_delete"] == "on":
           lang = get_lang(guild.id, "modlog")            

           embed=discord.Embed(color=0x7BCDE8)
           embed.set_author(name=str(lang["delet_am"]), icon_url=guild.icon_url)
           embed.add_field(name=str(lang["count"]), value=len(messages))
           timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
           time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))          
           embed.add_field(name=str(lang["time"]), value=f"``{time}``", inline=True)
           embed.add_field(name=str(lang["channel"]), value=channel.mention)
           for message in messages:
             criada = message.created_at.strftime('%H:%M:%S - %d/%m/20%y')
             user = message.author
             if user.bot == True:
                return
             if len(message.attachments) >=1:
                link = message.attachments[0].url
                url = str(link).replace("https://cdn.discordapp.com/","https://media.discordapp.net/")
             else:
               link = "None"
             if len(message.content) >=1:
                texto = message.content
             else:
               texto = "None"                   
                                   
             log = f"[{criada}] ({user.id}) {user} : {texto} - {link}\n"
             logs.append(log)

           all_text = "".join(logs)
           embed.add_field(name=str(lang["link"]), value="[hastebin]("+haste(all_text)+")")
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           canal = discord.utils.get(guild.channels, id=int(guild_db["modlog"]["channel"]))
           if canal is None:
             return
           await canal.send(embed=embed)
###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))
