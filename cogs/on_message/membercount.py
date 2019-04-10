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
    async def on_member_join(self, member):
        if member == self.client.user:
            return
        try:
         guild_db = date_server_cache(member.guild.id)
         lang = get_lang(member.guild.id, "events")
         if guild_db["membercount"]["channel"] == None:
            return
         canal = discord.utils.get(member.guild.channels, id=int(guild_db["membercount_channel"]))
         if canal is None:
            return
         if guild_db["membercount"]["status"] == False:
            return
         json ={
             "E0":"<:num_zero:563051887461400586>",
             "E1":"<:num_um:563051882675961861>",
             "E2":"<:num_dois:563051873183989771>",
             "E3":"<:num_treis:563051887465725963>",
             "E4":"<:num_quatro:563051886823866378>",
             "E5":"<:num_cinco:563051870613012490>",
             "E6":"<:num_seis:563051887499280385>",
             "E7":"<:num_sete:563051887373582356>",
             "E8":"<:num_oito:563051881748758538>",
             "E9":"<:num_nove:563051875310632960>"
             }
         text = str(len(member.guild.members))
         for n in range(0, 10):
            text = text.replace(str(n), "E"+str(n))
         for n in range(0, 10):
            text = text.replace("E"+str(n), json["E"+str(n)])                                                  
         texto = str(lang["member_count"]).format(text)
         await canal.edit(topic=texto)      
        except Exception as e:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member == self.client.user:
            return
        try:
         guild_db = date_server_cache(member.guild.id)
         lang = get_lang(member.guild.id, "events")
         if guild_db["membercount"]["channel"] == None:
            return
         canal = discord.utils.get(member.guild.channels, id=int(guild_db["membercount_channel"]))
         if canal is None:
            return
         if guild_db["membercount"]["status"] == False:
            return
         json ={
             "E0":"<:num_zero:563051887461400586>",
             "E1":"<:num_um:563051882675961861>",
             "E2":"<:num_dois:563051873183989771>",
             "E3":"<:num_treis:563051887465725963>",
             "E4":"<:num_quatro:563051886823866378>",
             "E5":"<:num_cinco:563051870613012490>",
             "E6":"<:num_seis:563051887499280385>",
             "E7":"<:num_sete:563051887373582356>",
             "E8":"<:num_oito:563051881748758538>",
             "E9":"<:num_nove:563051875310632960>"
             }
         text = str(len(member.guild.members))
         for n in range(0, 10):
            text = text.replace(str(n), "E"+str(n))
         for n in range(0, 10):
            text = text.replace("E"+str(n), json["E"+str(n)])                                                  
         texto = str(lang["member_count"]).format(text)
         await canal.edit(topic=texto)      
        except Exception as e:
            pass
###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(on_message(client))

