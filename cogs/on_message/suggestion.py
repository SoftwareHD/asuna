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

lista = [":recusado:562727385380683804",":aceito:562727385695256586"]
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
        try:
         guild_db = date_server_cache(message.guild.id)
         if guild_db["suggestion_channel"] == None:
            return
         if guild_db["suggestion_status"] == False:
            return
         if int(message.channel.id) == int(guild_db["suggestion_channel"]): 
           for reaction in lista:
            await message.add_reaction(reaction)
        except Exception as e:
            print(e)
###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))

