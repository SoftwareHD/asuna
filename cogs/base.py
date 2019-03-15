###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
from config import config
from config import get_lang
from config import get_rank

###########################################
# Class reformulada
###########################################

class base(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def base(self,ctx):
       await ctx.send("Cmd base")

###########################################
# Função leitura do cog
###########################################

def setup(client):
    print("[Bot] : Cmd (base) ")
    client.add_cog(base(client))
