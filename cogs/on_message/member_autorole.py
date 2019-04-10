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
    async def on_member_join(self, member):
        if member == self.client.user:
            return
        guild_db = date_server_cache(member.guild.id)
        if guild_db["autorole"]["status"] == False:
           return
        if guild_db["autorole"]["role"] == None:
           return           
        try:
          user = discord.utils.get(member.guild.members, id=int(member.id))
          role = discord.utils.get(member.guild.roles, id=int(guild_db["autorole"]["role"]))
          if role is None:
             return
          if user is None:
             return
          await user.add_roles(role)
        except:
            pass

# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))
