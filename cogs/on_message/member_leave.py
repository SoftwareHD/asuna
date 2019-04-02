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
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests

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
    async def on_member_remove(self, member):
        if member == self.client.user:
            return
        guild_db = date_server_cache(member.guild.id)
        lang = get_lang(member.guild.id, "events")
        if guild_db["leave_type"] == "1":
           if guild_db["leave_channel"] == None:
              return 
           if guild_db["leave_text"] == None:
              return
           channel = discord.utils.get(member.guild.channels, id=int(guild_db["leave_channel"]))
           await channel.send(guild_db["leave_text"])

        if guild_db["leave_type"] == "2":
           if guild_db["leave_channel"] == None:
              return 
           if guild_db["leave_text"] == None:
              return
           embed=discord.Embed(description=str(guild_db["leave_text"]), color=0x7BCDE8)
           member_text = str(lang["member_join"]).format(member)
           embed.set_author(name=str(member_text), icon_url=member.avatar_url)
           embed.set_thumbnail(url=member.avatar_url)
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           channel = discord.utils.get(member.guild.channels, id=int(guild_db["leave_channel"]))
           await channel.send(embed=embed,content=member.mention)
        if guild_db["leave_type"] == "3":           
           if guild_db["leave_channel"] == None:
              return 
           if guild_db["leave_text"] == None:
              return
           url = requests.get(member.avatar_url)
           avatar = Image.open(BytesIO(url.content))
           avatar = avatar.resize((245, 245));
           bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
           mask = Image.new('L', bigsize, 0)
           draw = ImageDraw.Draw(mask)
           draw.ellipse((0, 0) + bigsize, fill=255)
           mask = mask.resize(avatar.size, Image.ANTIALIAS)
           avatar.putalpha(mask)
           saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
           saida.putalpha(mask)
           fundo = Image.open('./files/gd.png')
           fonte = ImageFont.truetype('./files/ariblk.ttf',42)
           fonte2 = ImageFont.truetype('./files/ariblk.ttf',49)
           escrever = ImageDraw.Draw(fundo)
           user = str(member.name)
           if len(user) >= 18:
             user_txt = user[:15]+"..."
           else:
             user_txt = user
           server = str(member.guild.name)
           if len(server) >= 18:
             server_txt = server[:15]+"..."
           else:
             server_txt = server   
           escrever.text(xy=(365,135), text=str(user_txt),fill=(57, 156, 200),font=fonte)
           escrever.text(xy=(398,215), text=str(member.discriminator),fill=(57, 156, 200),font=fonte2)
           escrever.text(xy=(365,305), text=str(server_txt),fill=(57, 156, 200),font=fonte)
           fundo.paste(avatar, (45, 113), avatar)
           fundo.save("./files/leave.png")
           arquivo = discord.File("./files/leave.png", filename="leave.png")
           embed = discord.Embed(color=0x7BCDE8)
           embed.set_image(url="attachment://leave.png")
           channel = discord.utils.get(member.guild.channels, id=int(guild_db["leave_channel"]))
           await channel.send(file=arquivo, embed=embed, content=member.mention)



# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))